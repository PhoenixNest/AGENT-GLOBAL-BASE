# UIKit Integration

## UIKit Integration

### UIControl Publishers

UIKit controls do not natively publish events. Use extensions to bridge UIControl target-action to Combine publishers.

```swift
// UITextField text changes publisher
extension UITextField {
    var textPublisher: AnyPublisher<String, Never> {
        NotificationCenter.default
            .publisher(for: UITextField.textDidChangeNotification, object: self)
            .compactMap { ($0.object as? UITextField)?.text ?? "" }
            .eraseToAnyPublisher()
    }
}

// UIButton tap publisher
extension UIButton {
    var tapPublisher: AnyPublisher<Void, Never> {
        let subject = PassthroughSubject<Void, Never>()
        addTarget(
            closurePublisher(target: subject) { _ in subject.send(()) }
        )
        return subject.eraseToAnyPublisher()
    }
}

// UISwitch value publisher
extension UISwitch {
    var valuePublisher: AnyPublisher<Bool, Never> {
        NotificationCenter.default
            .publisher(for: UIControl.valueChangedNotification, object: self)
            .map { ($0.object as? UISwitch)?.isOn ?? false }
            .eraseToAnyPublisher()
    }
}
```

### NotificationCenter Publishers

`NotificationCenter` natively publishes via the `publisher(for:object:)` method:

```swift
NotificationCenter.default
    .publisher(for: UIApplication.didEnterBackgroundNotification)
    .sink { _ in
        // Handle background transition
    }
    .store(in: &cancellables)

// Keyboard notifications with value extraction
NotificationCenter.default
    .publisher(for: UIResponder.keyboardWillShowNotification)
    .compactMap { notification in
        notification.userInfo?[UIResponder.keyboardFrameEndUserInfoKey] as? CGRect
    }
    .sink { keyboardFrame in
        // Adjust layout for keyboard
    }
    .store(in: &cancellables)
```

---
