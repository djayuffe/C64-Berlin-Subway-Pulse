# Complete effect gallery

The production dispatch contains 26 active scenes. Each image is a native
384×272 VICE frame from the corresponding review build; the assembler-time
`START_PART` selector makes scene selection deterministic.

| # | Effect | Description | Runtime screenshot |
|---:|---|---|---|
| 0 | Title pulse field | Opens the journey with a restrained title field and music-reactive colour motion. | ![Title pulse field](screenshots/effects/effect-0.png) |
| 1 | Plasma storm | Interfering phase tables create a continuously changing plasma surface. | ![Plasma storm](screenshots/effects/effect-1.png) |
| 2 | Hyperspace | Fixed-point stars accelerate outward from a shared vanishing point. | ![Hyperspace](screenshots/effects/effect-2.png) |
| 3 | XOR moire | XOR interference produces sharp rotating diamonds and high-contrast bands. | ![XOR moire](screenshots/effects/effect-3.png) |
| 4 | Waves | Sine-displaced horizontal colour bands sweep across the character field. | ![Waves](screenshots/effects/effect-4.png) |
| 5 | Perspective tunnel | XMUL perspective, barrel warp, and forward-Z phases form a moving tunnel. | ![Perspective tunnel](screenshots/effects/effect-5.png) |
| 6 | Sine starfield | Fast and slow star populations drift in parallax with glowing points. | ![Sine starfield](screenshots/effects/effect-6.png) |
| 7 | Text wireframe | Row-safe text-mode geometry adapts a wireframe grid to the C64 character screen. | ![Text wireframe](screenshots/effects/effect-7.png) |
| 8 | Heart Voyager trail | A heart silhouette receives a moving golden trail and halo treatment. | ![Heart Voyager trail](screenshots/effects/effect-8.png) |
| 9 | Multiplex cube | Alternating edge bars translate sprite-multiplex timing ideas into text mode. | ![Multiplex cube](screenshots/effects/effect-9.png) |
| 10 | Yaw wobble tunnel | Column wobble and per-cell tint give the tunnel a controlled side-to-side sweep. | ![Yaw wobble tunnel](screenshots/effects/effect-10.png) |
| 11 | Turbo boot tunnel | A faster boot-grid tunnel uses automatic zoom phases and pulse timing. | ![Turbo boot tunnel](screenshots/effects/effect-11.png) |
| 12 | Golden halo heart | A distinct animated golden halo surrounds the heart form. | ![Golden halo heart](screenshots/effects/effect-12.png) |
| 13 | Raster grid boot | Layered grid rows and raster colour changes create a boot-up field. | ![Raster grid boot](screenshots/effects/effect-13.png) |
| 14 | Cyber grid | A neon matrix-floor adaptation combines grid geometry with SID colour response. | ![Cyber grid](screenshots/effects/effect-14.png) |
| 15 | Safe tunnel prime | A conservative tunnel variant uses bounded arithmetic and stable row ownership. | ![Safe tunnel prime](screenshots/effects/effect-15.png) |
| 16 | Black orbit field | Orbital rings fold around a dark centre to suggest a black-hole field. | ![Black orbit field](screenshots/effects/effect-16.png) |
| 17 | Rotor cube final | A corrected 16-step cube uses projected front/back rectangles and sparse connectors. | ![Rotor cube final](screenshots/effects/effect-17.png) |
| 18 | Solar flare | A radial flare expands bright colour energy from a central origin. | ![Solar flare](screenshots/effects/effect-18.png) |
| 19 | Prism gate | Layered gate bars open around a colour-shifting central passage. | ![Prism gate](screenshots/effects/effect-19.png) |
| 20 | Twist lattice | Phase-shifted lattice lines twist through character and colour tables. | ![Twist lattice](screenshots/effects/effect-20.png) |
| 21 | Infinity corridor | Distance tables, column warp, and palette cycling create an endless corridor. | ![Infinity corridor](screenshots/effects/effect-21.png) |
| 22 | Gold trench | Perspective rails, inner glow, vanishing markers, and beat crossbars define the trench. | ![Gold trench](screenshots/effects/effect-22.png) |
| 23 | Cube V3 rotor | A stable 3D cube draws front/rear planes, joints, and depth connectors. | ![Cube V3 rotor](screenshots/effects/effect-23.png) |
| 24 | Mux edge field | Alternating edge bands convert multiplex timing into safe character geometry. | ![Mux edge field](screenshots/effects/effect-24.png) |
| 25 | Final pulse closure | The safe final slot adds mirrored sparks and a centre heartbeat without touching row 24. | ![Final pulse closure](screenshots/effects/effect-25.png) |

## Reproduce one frame

```sh
cd src
acme -DSTART_PART=25 -f cbm -o ../build/review-effect-25.prg subway.s
x64sc -autostartprgmode 1 -autostart ../build/review-effect-25.prg
```

Regenerate all captures with `./tools/capture_effects.sh`.
