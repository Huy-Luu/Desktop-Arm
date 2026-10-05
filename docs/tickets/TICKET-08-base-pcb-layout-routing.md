# TICKET-08: Base PCB Layout, 2-Layer Routing, and Dock Pad Footprint

- **Status**: Blocked
- **Blocked By**: TICKET-07
- **Delivers**: Complete 2-layer PCB layout with thermal copper pours for TMC2209 and buck regulator, 24V high-current motor traces, and top-deck gold contact pads for Desktop Assistant docking.

## Acceptance Criteria
1. 2-layer PCB within $100\text{mm} \times 100\text{mm}$ standard fabrication bounds.
2. Star-ground layout isolating noisy 24V stepper return currents from 3.3V MCU analog/digital ground.
3. Top-side ENIG gold circular landing pads matching Desktop Assistant `KZM05P03UFT2-B` pogo pin dimensions.
4. DRC checks pass with zero unrouted nets.
