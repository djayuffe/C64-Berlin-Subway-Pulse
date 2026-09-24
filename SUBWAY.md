# Berlin Trip Subway — v1.2.4

Final-pulse-polish release.

Controls:
- SPACE: skip current part/card
- +: faster scroller
- -: slower scroller

Safety closure:
- Black Orbit 2 removed from final slot
- final slot uses safe `fc_init` / `fc_update`
- final pulse adds mirrored safe sparks and centre heartbeat
- split scroller IRQ owns `$d016`
- row 24 remains reserved for global scroller
- DemoReturnToReady jumps to BASIC warm start
