# Execution Guidance

## Execution Guidance

### React Native Component Architecture

```typescript
// Component library structure
// src/components/
//   ├── Button/
//   │   ├── Button.tsx
//   │   ├── Button.styles.ts
//   │   └── index.ts
//   ├── Card/
//   ├── Input/
//   ├── Modal/
//   └── index.ts  // Barrel export

// Button component with variants
type ButtonVariant = 'primary' | 'secondary' | 'outline' | 'ghost';
type ButtonSize = 'sm' | 'md' | 'lg';

interface ButtonProps extends TouchableOpacityProps {
  variant?: ButtonVariant;
  size?: ButtonSize;
  isLoading?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  children: React.ReactNode;
}

export const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'md',
  isLoading = false,
  leftIcon,
  rightIcon,
  children,
  disabled,
  style,
  ...rest
}) => {
  const buttonStyle = useMemo(
    () => [styles.base, styles[variant], styles[size], disabled && styles.disabled],
    [variant, size, disabled]
  );

  return (
    <TouchableOpacity
      style={buttonStyle}
      disabled={disabled || isLoading}
      activeOpacity={0.7}
      {...rest}
    >
      {isLoading ? (
        <ActivityIndicator color={getTextColor(variant)} />
      ) : (
        <>
          {leftIcon}
          <Text style={[styles.text, styles[`${variant}Text`], styles[`${size}Text`]]}>
            {children}
          </Text>
          {rightIcon}
        </>
      )}
    </TouchableOpacity>
  );
};

// Custom hook for form management
function useForm<T extends Record<string, any>>(initialValues: T, validationSchema: Yup.Schema<T>) {
  const [values, setValues] = useState<T>(initialValues);
  const [errors, setErrors] = useState<Partial<Record<keyof T, string>>>({});
  const [touched, setTouched] = useState<Partial<Record<keyof T, boolean>>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const setValue = useCallback(<K extends keyof T>(key: K, value: T[K]) => {
    setValues(prev => ({ ...prev, [key]: value }));
    // Clear error on change
    setErrors(prev => ({ ...prev, [key]: undefined }));
  }, []);

  const validate = useCallback(async (): Promise<boolean> => {
    try {
      await validationSchema.validate(values, { abortEarly: false });
      setErrors({});
      return true;
    } catch (err) {
      if (err instanceof Yup.ValidationError) {
        const newErrors: Partial<Record<keyof T, string>> = {};
        err.inner.forEach(e => {
          if (e.path) newErrors[e.path as keyof T] = e.message;
        });
        setErrors(newErrors);
      }
      return false;
    }
  }, [values, validationSchema]);

  const handleSubmit = useCallback(async (onSubmit: (values: T) => Promise<void>) => {
    const isValid = await validate();
    if (!isValid) return;

    setIsSubmitting(true);
    try {
      await onSubmit(values);
    } finally {
      setIsSubmitting(false);
    }
  }, [validate]);

  return { values, errors, touched, isSubmitting, setValue, handleSubmit, validate };
}
```

### Native Module Bridges

**iOS Native Module (Swift):**

```swift
// BiometricModule.swift
@objc(BiometricModule)
class BiometricModule: NSObject {

  @objc
  static func requiresMainQueueSetup() -> Bool {
    return false
  }

  @objc
  func isAvailable(_ resolve: @escaping RCTPromiseResolveBlock,
                   reject: @escaping RCTPromiseRejectBlock) {
    let context = LAContext()
    var error: NSError?

    let available = context.canEvaluatePolicy(.deviceOwnerAuthenticationWithBiometrics, error: &error)

    if available {
      let biometryType = context.biometryType == .faceID ? "faceID" : "touchID"
      resolve(["available": true, "type": biometryType])
    } else {
      resolve(["available": false, "type": nil, "error": error?.localizedDescription])
    }
  }

  @objc
  func authenticate(_ prompt: String,
                    resolve: @escaping RCTPromiseResolveBlock,
                    reject: @escaping RCTPromiseRejectBlock) {
    let context = LAContext()
    context.localizedReason = prompt

    context.evaluatePolicy(.deviceOwnerAuthenticationWithBiometrics) { success, error in
      DispatchQueue.main.async {
        if success {
          resolve(["success": true])
        } else {
          let laError = error as? LAError
          reject(
            laError?.code.stringValue ?? "unknown",
            error?.localizedDescription ?? "Authentication failed",
            error
          )
        }
      }
    }
  }
}

// Swift Bridging Header
// #import <React/RCTBridgeModule.h>

// Module registration
@objc
class BiometricModuleBridge: NSObject, RCTBridgeModule {
  static func moduleName() -> String! {
    return "BiometricModule"
  }

  static func requiresMainQueueSetup() -> Bool {
    return false
  }
}
```

**Android Native Module (Kotlin):**

```kotlin
// BiometricModule.kt
class BiometricModule(reactContext: ReactApplicationContext) :
    ReactContextBaseJavaModule(reactContext) {

    override fun getName(): String = "BiometricModule"

    @ReactMethod
    fun isAvailable(promise: Promise) {
        val biometricManager = BiometricManager.from(reactApplicationContext)
        val canAuthenticate = biometricManager.canAuthenticate(
            BiometricManager.Authenticators.BIOMETRIC_STRONG
        )

        val result = Arguments.createMap()
        when (canAuthenticate) {
            BiometricManager.BIOMETRIC_SUCCESS -> {
                result.putBoolean("available", true)
                result.putString("type", "fingerprint") // Android doesn't distinguish in API
            }
            BiometricManager.BIOMETRIC_ERROR_NO_HARDWARE -> {
                result.putBoolean("available", false)
                result.putString("error", "No biometric hardware")
            }
            BiometricManager.BIOMETRIC_ERROR_NONE_ENROLLED -> {
                result.putBoolean("available", false)
                result.putString("error", "No biometrics enrolled")
            }
            else -> {
                result.putBoolean("available", false)
                result.putString("error", "Biometric not available")
            }
        }
        promise.resolve(result)
    }

    @ReactMethod
    fun authenticate(prompt: String, promise: Promise) {
        val activity = currentActivity
        if (activity == null) {
            promise.reject("NO_ACTIVITY", "No current activity")
            return
        }

        val biometricPrompt = BiometricPrompt(
            activity,
            ContextCompat.getMainExecutor(reactApplicationContext),
            object : BiometricPrompt.AuthenticationCallback() {
                override fun onAuthenticationSucceeded(result: BiometricPrompt.AuthenticationResult) {
                    super.onAuthenticationSucceeded(result)
                    val response = Arguments.createMap()
                    response.putBoolean("success", true)
                    promise.resolve(response)
                }

                override fun onAuthenticationError(errorCode: Int, errString: CharSequence) {
                    super.onAuthenticationError(errorCode, errString)
                    promise.reject("AUTH_ERROR_$errorCode", errString.toString())
                }

                override fun onAuthenticationFailed() {
                    super.onAuthenticationFailed()
                    promise.reject("AUTH_FAILED", "Authentication failed")
                }
            }
        )

        val promptInfo = BiometricPrompt.PromptInfo.Builder()
            .setTitle("Biometric Authentication")
            .setSubtitle(prompt)
            .setNegativeButtonText("Use Password")
            .build()

        biometricPrompt.authenticate(promptInfo)
    }
}

// Package registration
class BiometricPackage : ReactPackage {
    override fun createNativeModules(reactContext: ReactApplicationContext): List<NativeModule> {
        return listOf(BiometricModule(reactContext))
    }

    override fun createViewManagers(reactContext: ReactApplicationContext): List<ViewManager<*, *>> {
        return emptyList()
    }
}
```

**TypeScript interface for native module:**

```typescript
// src/native/BiometricModule.ts
import { NativeModules } from 'react-native';

interface BiometricResult {
  available: boolean;
  type?: 'faceID' | 'touchID' | 'fingerprint';
  error?: string;
}

interface BiometricModule {
  isAvailable(): Promise<BiometricResult>;
  authenticate(prompt: string): Promise<{ success: boolean }>;
}

const { BiometricModule } = NativeModules;
export default BiometricModule as BiometricModule;

// Usage
export async function authenticateWithBiometrics(prompt: string): Promise<boolean> {
  const { available } = await BiometricModule.isAvailable();
  if (!available) {

```

    return false;

}

try {
const result = await BiometricModule.authenticate(prompt);
return result.success;
} catch (error: any) {
if (error.code === 'AUTH_ERROR_USER_FALLBACK') {
// User chose password fallback
return false;
}
throw error;
}
}

````

### Document Scanning with react-native-vision-camera

```typescript
import { useCameraDevices, Camera, Frame } from 'react-native-vision-camera';
import { runOnJS } from 'react-native-reanimated';

export function DocumentScanner({ onDocumentDetected }: ScannerProps) {
  const devices = useCameraDevices();
  const device = devices.back;
  const [hasPermission, requestPermission] = useCameraPermission();
  const [scanning, setScanning] = useState(true);

  useEffect(() => {
    if (!hasPermission) {
      requestPermission();
    }
  }, [hasPermission, requestPermission]);

  // Frame processor for document detection
  const frameProcessor = useFrameProcessor(
    (frame: Frame) => {
      'worklet';

      // Run document detection on native side
      const result = detectDocument(frame);

      if (result.isDocument && result.confidence > 0.8) {
        // Capture the frame
        runOnJS(onDocumentDetected)({
          corners: result.corners,
          confidence: result.confidence,
        });
      }
    },
    [onDocumentDetected]
  );

  if (!device || !hasPermission) {
    return <PermissionRequest />;
  }

  return (
    <View style={styles.container}>
      <Camera
        style={StyleSheet.absoluteFill}
        device={device}
        isActive={scanning}
        frameProcessor={frameProcessor}
        frameProcessorFps={5} // 5 FPS for document detection
        photo={true}
      />

      {/* Document detection overlay */}
      <DocumentOverlay scanning={scanning} />

      {/* Controls */}
      <View style={styles.controls}>
        <Button
          title="Capture"
          onPress={handleManualCapture}
        />
        <Button
          title="Cancel"
          variant="outline"
          onPress={() => setScanning(false)}
        />
      </View>
    </View>
  );
}

// Native document detection (iOS Vision framework)
// DocumentDetector.mm
#import <Vision/Vision.h>

RCT_EXTERN_METHOD(detectDocument:(CMSampleBufferRef)frame
                  resolver:(RCTPromiseResolveBlock)resolve
                  rejecter:(RCTPromiseRejectBlock)reject)

// Detect document in frame using VNDetectRectanglesRequest
- (void)detectDocument:(CMSampleBufferRef)frame
              resolver:(RCTPromiseResolveBlock)resolve
              rejecter:(RCTPromiseRejectBlock)reject {

    VNImageRequestHandler *handler = [[VNImageRequestHandler alloc]
        initWithCMSampleBuffer:frame options:@{}];

    VNDetectRectanglesRequest *request = [[VNDetectRectanglesRequest alloc] init];
    request.minimumConfidence = 0.8;
    request.maximumObservations = 1;
    request.quadratureTolerance = 10.0;

    NSError *error = nil;
    [handler performRequests:@[request] error:&error];

    if (error) {
        reject(@"DETECTION_ERROR", error.localizedDescription, error);
        return;
    }

    if (request.results.count > 0) {
        VNRectangleObservation *observation = request.results.firstObject;
        resolve(@{
            @"isDocument": @YES,
            @"confidence": @(observation.confidence),
            @"corners": @{
                @"topLeft": [self pointToDict:observation.topLeft],
                @"topRight": [self pointToDict:observation.topRight],
                @"bottomRight": [self pointToDict:observation.bottomRight],
                @"bottomLeft": [self pointToDict:observation.bottomLeft],
            }
        });
    } else {
        resolve(@{@"isDocument": @NO, @"confidence": @0});
    }
}
````

### Cross-Platform UI Patterns

```typescript
// Platform-specific styling
import { Platform, StyleSheet } from 'react-native';

const styles = StyleSheet.create({
  card: {
    borderRadius: 12,
    padding: 16,
    // Platform-specific shadow
    ...Platform.select({
      ios: {
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.1,
        shadowRadius: 4,
      },
      android: {
        elevation: 4,
      },
    }),
  },

  input: {
    height: 48,
    borderWidth: 1,
    borderRadius: 8,
    paddingHorizontal: 12,
    // Platform-specific font
    ...Platform.select({
      ios: {
        fontSize: 16, // Prevents zoom on iOS
      },
      android: {
        fontSize: 14,
      },
    }),
  },
});

// Responsive layout hook
function useResponsiveLayout() {
  const { width, height } = useWindowDimensions();
  const isTablet = width >= 768;
  const isLandscape = width > height;

  return {
    width,
    height,
    isTablet,
    isLandscape,
    gridColumns: isTablet ? 2 : 1,
    isSmallScreen: width < 375,
  };
}

// Dark mode support
import { useColorScheme } from 'react-native';

function useTheme() {
  const colorScheme = useColorScheme();
  const isDark = colorScheme === 'dark';

  return {
    isDark,
    colors: isDark ? darkColors : lightColors,
    scheme: colorScheme,
  };
}

const lightColors = {
  background: '#FFFFFF',
  surface: '#F8F9FA',
  text: '#1A1A1A',
  textSecondary: '#666666',
  border: '#E0E0E0',
  primary: '#007AFF',
  error: '#FF3B30',
};

const darkColors = {
  background: '#000000',
  surface: '#1C1C1E',
  text: '#FFFFFF',
  textSecondary: '#999999',
  border: '#333333',
  primary: '#0A84FF',
  error: '#FF453A',
};

// Accessibility-first component
export function AccessibleButton({
  label,
  onPress,
  disabled,
  role = 'button',
  ...rest
}: AccessibleButtonProps) {
  return (
    <TouchableOpacity
      accessibilityRole={role}
      accessibilityLabel={label}
      accessibilityState={{ disabled }}
      accessibilityHint={disabled ? 'This button is disabled' : `Activates ${label}`}
      accessible={true}
      onPress={onPress}
      disabled={disabled}
      {...rest}
    />
  );
}
```
