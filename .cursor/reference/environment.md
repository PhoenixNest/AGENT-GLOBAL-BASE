# Development Environment Reference

## Hardware — Asus Zenbook Pro 14 Duo OLED (UX8402VV)

| Component             | Specification                                                                                                                      |
| --------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| **Model**             | Asus Zenbook Pro 14 Duo OLED UX8402VV                                                                                              |
| **Category**          | Dual-screen creator laptop                                                                                                         |
| **CPU**               | Intel Core i7-13700H (Raptor Lake-H) — 14 cores / 20 threads (6× P-Cores @ 5.0 GHz, 8× E-Cores @ 3.7 GHz)                          |
| **GPU**               | NVIDIA GeForce RTX 4060 Laptop — 8 GB GDDR6 VRAM                                                                                   |
| **RAM**               | 32 GB DDR5                                                                                                                         |
| **Storage**           | M.2 NVMe PCIe 4.0 SSD (1 TB base, expandable via M.2 2280 slot)                                                                    |
| **Primary Display**   | 14.5" OLED, 16:10, 2880×1800 (234 PPI), 120 Hz, 0.2ms, 550 nits HDR, 100% DCI-P3, PANTONE Validated, Glossy, Touch, Stylus support |
| **Secondary Display** | 12.7" ScreenPad Plus, IPS, 2880×864, Glossy, Stylus support                                                                        |
| **I/O Ports**         | 2× Thunderbolt 4 (USB-C), 1× USB 3.2 Gen 2 Type-A, 1× HDMI, 1× 3.5mm Combo Audio Jack, 1× DC-in (ø6.0), 1× microSD Card Reader     |
| **Networking**        | Wi-Fi 6E (802.11ax, 2×2, 6 GHz), Bluetooth 5.3                                                                                     |
| **Camera**            | FHD (1080p) with IR function — Windows Hello support                                                                               |
| **Audio**             | Smart Amp Technology, Built-in array microphone, Built-in stereo speakers                                                          |
| **Keyboard**          | Backlit Chiclet Keyboard, Precision Touchpad                                                                                       |
| **Stylus**            | ASUS Pen SA203H-MPP2.0 (included)                                                                                                  |
| **Battery**           | 76 WHrs, 4S1P, 4-cell Li-ion                                                                                                       |
| **Power Adapter**     | 180W (20V/9A), 100~240V AC 50/60Hz universal                                                                                       |
| **Weight**            | 1.75 kg (3.86 lbs)                                                                                                                 |
| **Dimensions**        | 32.25 × 22.47 × 1.79~1.96 cm (12.70" × 8.85" × 0.70"~0.77")                                                                        |
| **Security**          | TPM 2.0, IR Webcam (Windows Hello), US MIL-STD 810H                                                                                |
| **OS**                | Windows 11 Home                                                                                                                    |

## Software Environment

| Tool       | Path                                        | Notes                                           |
| ---------- | ------------------------------------------- | ----------------------------------------------- |
| Python     | `C:\Program Files\Python\313\python.exe`    | Use `python`, NOT `python3`                     |
| Git Bash   | `C:\Program Files\Git\bin\bash.exe`         | Available                                       |
| Shell      | `cmd.exe` (primary), PowerShell (secondary) | Git bash has pipe/subprocess issues with Python |
| Cursor IDE | Local installation                          | Cursor AI Agent with integrated toolset         |

## Critical Rules for This Environment

| Rule                                       | Rationale                                                                              |
| ------------------------------------------ | -------------------------------------------------------------------------------------- |
| **Use `python`, not `python3`**            | Windows installation uses `python.exe`; `python3` is a non-functional WindowsApps stub |
| **Avoid `xxd`, `/dev/urandom` in scripts** | Not reliably available in Git bash. Use Python's `hashlib` and `random` instead        |
