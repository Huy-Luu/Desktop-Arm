# TICKET-06: Base Controller KiCad Schematic: 24V Power, Buck & Pogo Dock

- **Status**: Ready
- **Blocked By**: None
- **Delivers**: KiCad schematic for Arm Base Controller board power entry (24V DC), `TPS54302` 5V 3A buck converter, 3.3V LDO, and 5-pin ENIG pogo dock matching Desktop Assistant's `KZM05P03UFT2-B`.

## Acceptance Criteria
1. 24V DC input with `SMBJ28A` TVS diode and P-channel MOSFET reverse polarity protection.
2. `TPS54302` step-down buck converter stepping 24V to 5.0V @ 3A with $<30\text{mV}$ ripple.
3. 5-pin pogo pin dock footprint with 2A PPTC fuse and ESD protection array (`USBLC6-2SC6`).
4. Active-low `DOCK_DETECT_N` interrupt line with pullup and debounce cap to MCU.
