# Flutter i18n

**Category:** Mobile Engineering — Cross-Platform Localization
**Owner:** Cross-Platform Engineer (Fatima Al-Zahra)

## Overview

This skill implements Flutter internationalization covering ARB file management, pluralization, RTL layout support, locale switching at runtime, and integration with the Localization Department's TMS pipeline. It applies to Stage 5 (Development) where all strings are externalized for translation, Stage 9 (i18n Engineering) where the two-phase localization process is executed, and Stage 10 (Release Readiness) where translation completeness is verified.

## Competency Dimensions

| Dimension        | Description                                                                                            | Proficiency Indicators                                                                                                                               |
| ---------------- | ------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| Flutter intl     | flutter_localizations setup, Intl.message, Intl.plural, Intl.select, date/number formatting            | All user-facing strings use Intl or AppLocalizations; date/number formatting respects locale; no hardcoded strings in widgets                        |
| ARB Files        | ARB structure, placeholder metadata, attribute annotations, gen_l10n configuration, ARB validation     | ARB files follow consistent structure; placeholders have proper metadata; gen_l10n generates type-safe localization class                            |
| Pluralization    | Intl.plural with all forms, zero/one/two/few/many/other, locale-specific rules, gender-based selection | All plural forms implemented per CLDR rules; zero form handled for languages that require it; gender selection for languages with grammatical gender |
| RTL Support      | Directionality widget, RTL-aware layouts, mirror icons, text alignment, RTL testing                    | Full RTL layout support for Arabic/Hebrew; icons mirrored appropriately; text alignment adapts to direction; no hardcoded LTR assumptions            |
| Locale Switching | Runtime locale change, persistence, system locale detection, locale fallback, supported locales list   | Locale persists across app restarts; fallback to closest supported locale; system locale detected on first launch; locale switch is seamless         |

## Execution Guidance

### Flutter intl — Complete Setup

**pubspec.yaml configuration:**

```yaml
flutter:
  generate: true # Enable code generation

dependencies:
  flutter_localizations:
    sdk: flutter
  intl: ^0.19.0

dev_dependencies:
  flutter_gen: ^5.4.0
```

**l10n.yaml configuration:**

```yaml
arb-dir: lib/l10n
template-arb-file: app_en.arb
output-localization-file: app_localizations.dart
output-class: AppLocalizations
nullable-getter: false
synthetic-package: false
preferred-supported-locales:
  - en
  - ja
  - pt
  - ar
untranslated-messages-file: lib/l10n/untranslated.json
```

**MaterialApp configuration:**

```dart
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:flutter_gen/gen_l10n/app_localizations.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'My App',
      // Generated localizations
      localizationsDelegates: const [
        AppLocalizations.delegate,
        GlobalMaterialLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
        GlobalCupertinoLocalizations.delegate,
      ],
      supportedLocales: const [
        Locale('en'),       // English
        Locale('ja'),       // Japanese
        Locale('pt', 'BR'), // Brazilian Portuguese
        Locale('ar'),       // Arabic (RTL)
      ],
      // Locale resolution strategy
      localeResolutionCallback: (locale, supportedLocales) {
        if (locale == null) return supportedLocales.first;

        // Exact match
        for (var supported in supportedLocales) {
          if (supported.languageCode == locale.languageCode &&
              supported.countryCode == locale.countryCode) {
            return supported;
          }
        }

        // Language code match (fallback)
        for (var supported in supportedLocales) {
          if (supported.languageCode == locale.languageCode) {
            return supported;
          }
        }

        // Default fallback
        return supportedLocales.first;
      },
      home: const HomeScreen(),
    );
  }
}
```

### ARB Files — Production Structure

**app_en.arb (template):**

```json
{
  "@@locale": "en",
  "appTitle": "My Application",
  "@appTitle": {
    "description": "The main application title shown on the home screen"
  },
  "welcomeMessage": "Welcome, {userName}!",
  "@welcomeMessage": {
    "description": "Greeting message displayed after login",
    "placeholders": {
      "userName": {
        "type": "String",
        "example": "John"
      }
    }
  },
  "taskCount": "{count, plural, =0{No tasks} =1{1 task} other{{count} tasks}}",
  "@taskCount": {
    "description": "Number of tasks displayed in the task list header",
    "placeholders": {
      "count": {
        "type": "int",
        "example": 5
      }
    }
  },
  "lastUpdated": "Last updated {date}",
  "@lastUpdated": {
    "description": "Timestamp showing when data was last refreshed",
    "placeholders": {
      "date": {
        "type": "DateTime",
        "format": "yMMMd"
      }
    }
  },
  "greeting": "{gender, select, male{Hello sir} female{Hello ma'am} other{Hello}}",
  "@greeting": {
    "description": "Gender-specific greeting",
    "placeholders": {
      "gender": {
        "type": "String",
        "example": "male"
      }
    }
  },
  "deleteConfirmation": "Are you sure you want to delete this item?",
  "@deleteConfirmation": {
    "description": "Confirmation dialog message before deleting an item"
  },
  "confirmButton": "Confirm",
  "cancelButton": "Cancel",
  "deleteButton": "Delete",
  "searchPlaceholder": "Search...",
  "emptyState": "No results found",
  "errorNetwork": "Check your internet connection and try again",
  "errorServer": "We're experiencing technical difficulties. Please try again later",
  "errorUnknown": "An unexpected error occurred"
}
```

**app_ja.arb (Japanese translation):**

```json
{
  "@@locale": "ja",
  "appTitle": "マイアプリケーション",
  "welcomeMessage": "ようこそ、{userName}さん！",
  "taskCount": "{count, plural, =0{タスクなし} =1{1件のタスク} other{{count}件のタスク}}",
  "lastUpdated": "最終更新: {date}",
  "greeting": "{gender, select, male{こんにちは} female{こんにちは} other{こんにちは}}",
  "deleteConfirmation": "このアイテムを削除してもよろしいですか？",
  "confirmButton": "確認",
  "cancelButton": "キャンセル",
  "deleteButton": "削除",
  "searchPlaceholder": "検索...",
  "emptyState": "結果が見つかりません",
  "errorNetwork": "インターネット接続を確認して、もう一度お試しください",
  "errorServer": "技術的な問題が発生しています。後でもう一度お試しください",
  "errorUnknown": "予期しないエラーが発生しました"
}
```

**app_ar.arb (Arabic — RTL):**

```json
{
  "@@locale": "ar",
  "appTitle": "تطبيقي",
  "welcomeMessage": "!مرحباً، {userName}",
  "taskCount": "{count, plural, zero{لا توجد مهام} one{مهمة واحدة} two{مهمتان} few{{count} مهام} many{{count} مهمة} other{{count} مهمة}}",
  "lastUpdated": "آخر تحديث: {date}",
  "greeting": "{gender, select, male{أهلاً سيدي} female{أهلاً سيدتي} other{أهلاً}}",
  "deleteConfirmation": "هل أنت متأكد من حذف هذا العنصر؟",
  "confirmButton": "تأكيد",
  "cancelButton": "إلغاء",
  "deleteButton": "حذف",
  "searchPlaceholder": "...بحث",
  "emptyState": "لم يتم العثور على نتائج",
  "errorNetwork": "تحقق من اتصالك بالإنترنت وحاول مرة أخرى",
  "errorServer": "نحن نواجه صعوبات فنية. يرجى المحاولة لاحقاً",
  "errorUnknown": "حدث خطأ غير متوقع"
}
```

### Usage in Widgets

```dart
import 'package:flutter_gen/gen_l10n/app_localizations.dart';

class WelcomeScreen extends StatelessWidget {
  final String userName;

  const WelcomeScreen({super.key, required this.userName});

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context);

    return Scaffold(
      appBar: AppBar(
        title: Text(l10n.appTitle),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            // String with placeholder
            Text(l10n.welcomeMessage(userName)),

            const SizedBox(height: 16),

            // Pluralization
            Text(l10n.taskCount(taskCount)),

            const SizedBox(height: 16),

            // Date formatting
            Text(l10n.lastUpdated(lastUpdatedDate)),

            const SizedBox(height: 16),

            // Gender selection
            Text(l10n.greeting(userGender)),

            const SizedBox(height: 24),

            // Buttons
            FilledButton(
              onPressed: () => _confirm(context),
              child: Text(l10n.confirmButton),
            ),
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: Text(l10n.cancelButton),
            ),
          ],
        ),
      ),
    );
  }
}

// MARK: - Intl Direct Usage (for complex formatting)

class FormattedDateDisplay extends StatelessWidget {
  final DateTime date;

  const FormattedDateDisplay({super.key, required this.date});

  @override
  Widget build(BuildContext context) {
    final locale = Localizations.localeOf(context).languageCode;

    return Text(
      // DateFormat from intl package
      DateFormat.yMMMd(locale).format(date),
    );
  }
}

class FormattedNumberDisplay extends StatelessWidget {
  final double amount;
  final String currencyCode;

  const FormattedNumberDisplay({
    super.key,
    required this.amount,
    required this.currencyCode,
  });

  @override
  Widget build(BuildContext context) {
    final locale = Localizations.localeOf(context).languageCode;

    return Text(
      // NumberFormat from intl package
      NumberFormat.currency(
        locale: locale,
        symbol: currencyCode == 'USD' ? '\$' : currencyCode,
      ).format(amount),
    );
  }
}
```

### RTL Support — Complete Implementation

```dart
// MARK: - Directionality Widget

class RtlAwareScreen extends StatelessWidget {
  const RtlAwareScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final isRtl = Directionality.of(context) == TextDirection.rtl;

    return Scaffold(
      appBar: AppBar(
        title: const Text('RTL Aware'),
        // Leading/trailing automatically swap in RTL
        actions: [
          IconButton(
            icon: const Icon(Icons.settings),
            onPressed: () {},
          ),
        ],
      ),
      body: Directionality(
        // Explicitly set direction if needed
        textDirection: isRtl ? TextDirection.rtl : TextDirection.ltr,
        child: Column(
          children: [
            // Row automatically reverses in RTL
            Row(
              children: [
                const Icon(Icons.person),
                const SizedBox(width: 8),
                Text('User Name'),
                const Spacer(),
                // Icon automatically mirrored in RTL
                Transform(
                  transform: isRtl
                      ? Matrix4.rotationY(pi)
                      : Matrix4.identity(),
                  alignment: Alignment.center,
                  child: const Icon(Icons.arrow_forward),
                ),
              ],
            ),

            // Use start/end instead of left/right
            Padding(
              padding: const EdgeInsetsDirectional.only(
                start: 16,  // Left in LTR, Right in RTL
                end: 16,    // Right in LTR, Left in RTL
                top: 8,
                bottom: 8,
              ),
              child: Text('Directional padding'),
            ),
          ],
        ),
      ),
    );
  }
}

// MARK: - RTL-Aware Widget Patterns

// ✅ GOOD: Use DirectionalEdgeInsets
Padding(
  padding: const EdgeInsetsDirectional.only(start: 16, end: 8),
  child: Text('Content'),
)

// ✅ GOOD: Use MainAxisSize and CrossAxisAlignment
Row(
  mainAxisAlignment: MainAxisAlignment.start,  // Respects direction
  children: [/* ... */],
)

// ❌ BAD: Hardcoded left/right
Padding(
  padding: const EdgeInsets.only(left: 16, right: 8),  // Doesn't flip in RTL
  child: Text('Content'),
)

// ✅ GOOD: Use Align with AlignmentDirectional
Align(
  alignment: AlignmentDirectional.centerStart,  // Respects direction
  child: Text('Aligned text'),
)

// MARK: - Icon Mirroring

class DirectionalIcon extends StatelessWidget {
  final IconData icon;
  final double size;

  const DirectionalIcon({
    super.key,
    required this.icon,
    this.size = 24,
  });

  @override
  Widget build(BuildContext context) {
    final isRtl = Directionality.of(context) == TextDirection.rtl;

    // Icons that should be mirrored in RTL:
    // arrows, chevrons, back/forward, play/pause direction
    final shouldMirror = _mirrorInRtlIcons.contains(icon);

    return Transform(
      transform: (isRtl && shouldMirror)
          ? Matrix4.rotationY(pi)
          : Matrix4.identity(),
      alignment: Alignment.center,
      child: Icon(icon, size: size),
    );
  }

  static const _mirrorInRtlIcons = {
    Icons.arrow_back,
    Icons.arrow_forward,
    Icons.chevron_left,
    Icons.chevron_right,
    Icons.navigate_before,
    Icons.navigate_next,
    Icons.play_arrow,
    Icons.fast_forward,
    Icons.fast_rewind,
  };
}
```

### Runtime Locale Switching

```dart
// MARK: - Locale Provider

class LocaleProvider extends ChangeNotifier {
  Locale? _locale;
  Locale? get locale => _locale;

  final SharedPreferences _prefs;

  LocaleProvider(this._prefs) {
    _loadSavedLocale();
  }

  void _loadSavedLocale() {
    final savedLocale = _prefs.getString('preferred_locale');
    if (savedLocale != null) {
      final parts = savedLocale.split('_');
      _locale = parts.length > 1
          ? Locale(parts[0], parts[1])
          : Locale(parts[0]);
      notifyListeners();
    }
  }

  Future<void> setLocale(Locale newLocale) async {
    if (_locale == newLocale) return;

    _locale = newLocale;
    await _prefs.setString(
      'preferred_locale',
      newLocale.countryCode != null
          ? '${newLocale.languageCode}_${newLocale.countryCode}'
          : newLocale.languageCode,
    );
    notifyListeners();
  }

  Future<void> resetToSystemLocale() async {
    _locale = null;
    await _prefs.remove('preferred_locale');
    notifyListeners();
  }

  bool get isUsingSystemLocale => _locale == null;
}

// MARK: - MaterialApp with Locale Provider

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (_) => LocaleProvider(SharedPreferences.getInstance()),
      child: Consumer<LocaleProvider>(
        builder: (context, localeProvider, _) {
          return MaterialApp(
            locale: localeProvider.locale,
            localizationsDelegates: const [
              AppLocalizations.delegate,
              GlobalMaterialLocalizations.delegate,
              GlobalWidgetsLocalizations.delegate,
              GlobalCupertinoLocalizations.delegate,
            ],
            supportedLocales: const [
              Locale('en'),
              Locale('ja'),
              Locale('pt', 'BR'),
              Locale('ar'),
            ],
            home: const HomeScreen(),
          );
        },
      ),
    );
  }
}

// MARK: - Settings Screen

class LanguageSettingsScreen extends ConsumerWidget {
  const LanguageSettingsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final localeProvider = ref.watch(localeProviderProvider);
    final currentLocale = localeProvider.locale;

    final languages = [
      _LanguageOption('System', null),
      _LanguageOption('English', const Locale('en')),
      _LanguageOption('日本語', const Locale('ja')),
      _LanguageOption('Português', const Locale('pt', 'BR')),
      _LanguageOption('العربية', const Locale('ar')),
    ];

    return Scaffold(
      appBar: AppBar(title: const Text('Language')),
      body: ListView(
        children: languages.map((lang) {
          final isSelected = currentLocale == lang.locale;

          return RadioListTile<Locale?>(
            title: Text(lang.name),
            subtitle: lang.locale != null
                ? Text('${lang.locale!.languageCode}${lang.locale!.countryCode != null ? '_${lang.locale!.countryCode}' : ''}')
                : null,
            value: lang.locale,
            groupValue: currentLocale,
            onChanged: (locale) {
              if (locale == null) {
                localeProvider.resetToSystemLocale();
              } else {
                localeProvider.setLocale(locale);
              }
            },
          );
        }).toList(),
      ),
    );
  }
}

class _LanguageOption {
  final String name;
  final Locale? locale;
  const _LanguageOption(this.name, this.locale);
}
```

### TMS Integration — Stage 9 Process

```
┌─────────────────────────────────────────────────────────────┐
│ STAGE 9: i18n Engineering (Two-Phase Process)              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ Phase 1: R&D i18n Engineering (CTO-L + Platform Leads)     │
│   1. Extract all strings into ARB template (app_en.arb)     │
│   2. Validate ARB files with gen_l10n                       │
│   3. Run untranslated-messages-file check                   │
│   4. Verify RTL layout completeness                         │
│   5. Commit ARB files to repository                         │
│                                                             │
│ Phase 2: Localization Department TMS Translation            │
│   1. Export ARB files to TMS (Crowdin/Phrase/Localize)      │
│   2. Translators translate in TMS dashboard                 │
│   3. Import translated ARB files from TMS                   │
│   4. Run gen_l10n to regenerate AppLocalizations            │
│   5. Verify all translations render correctly               │
│   6. Translation Verification Report signed off by CTO-L    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**ARB validation script:**

```bash
#!/bin/bash
# validate_i18n.sh

echo "Validating i18n files..."

# Check gen_l10n compilation
flutter gen-l10n
if [ $? -ne 0 ]; then
    echo "❌ gen_l10n failed — check ARB file syntax"
    exit 1
fi

# Check for untranslated messages
if [ -f "lib/l10n/untranslated.json" ]; then
    UNTRANSLATED=$(cat lib/l10n/untranslated.json)
    if [ "$UNTRANSLATED" != "{}" ]; then
        echo "⚠️  Untranslated messages found:"
        echo "$UNTRANSLATED"
    fi
fi

# Check ARB key consistency across locales
TEMPLATE_KEYS=$(jq -r 'keys[]' lib/l10n/app_en.arb | grep -v '^@' | sort)
for arb in lib/l10n/app_*.arb; do
    LOCALE=$(jq -r '.@@locale' "$arb")
    FILE_KEYS=$(jq -r 'keys[]' "$arb" | grep -v '^@' | sort)

    MISSING=$(comm -23 <(echo "$TEMPLATE_KEYS") <(echo "$FILE_KEYS"))
    if [ -n "$MISSING" ]; then
        echo "❌ $LOCALE missing keys:"
        echo "$MISSING"
    fi
done

echo "✅ i18n validation complete"
```

## Pipeline Integration

- **Stage 5 (Development):** All user-facing strings externalized via ARB files. No hardcoded strings in widget code. RTL-aware layouts from the start.
- **Stage 9 (i18n Engineering):** Primary stage for this skill. Phase 1: R&D extracts strings and validates ARB files. Phase 2: Localization Department translates via TMS.
- **Stage 10 (Release Readiness):** Translation completeness verified. All target languages must have 100% translation coverage before release.

## Quality Standards

- **Zero** hardcoded user-facing strings in widget code — all strings in ARB files
- **100%** ARB files pass `flutter gen-l10n` compilation without errors
- All ARB placeholders have **metadata** (description, type, example)
- Pluralization uses **CLDR-compliant** forms — all required forms per language
- RTL layouts tested for **all RTL-supported languages** (Arabic, Hebrew)
- **DirectionalEdgeInsets** used instead of EdgeInsets (start/end vs left/right)
- Icons that imply direction are **mirrored in RTL** mode
- Locale preference **persists** across app restarts via SharedPreferences
- Runtime locale switching **rebuilds** the MaterialApp with new locale
- `untranslated-messages-file` checked on CI — **zero** untranslated messages for release
- Translation Verification Report **signed off** by CTO-L before Stage 10 release
- Date and number formatting **respects locale** — DateFormat and NumberFormat with locale parameter
- ARB files validated for **key consistency** across all locales — no missing keys
