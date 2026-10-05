# TICKET-11: ESP32-S3 Firmware: StallGuard4 Homing & S-Curve Stepper Engine

- **Status**: Blocked
- **Blocked By**: TICKET-07
- **Delivers**: Embedded firmware running on ESP32-S3 that performs sensorless homing on boot, executes jerk-limited S-curve stepper acceleration, and cuts power on stall detection.

## Acceptance Criteria
1. ESP-IDF project in `firmware/` with hardware timer step pulse generator running at up to 40 kHz.
2. Smooth jerk-limited S-curve trajectory acceleration avoiding structural vibrations.
3. Homing routine: moves axis at 200mA current until StallGuard `DIAG` pin fires $\to$ stops and zeros position coordinate $\to$ steps off 2mm.
4. Auto-stop: If StallGuard triggers during normal motion, immediately decelerates to zero and broadcasts collision event.
