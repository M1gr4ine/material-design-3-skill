// Unit-mass M3 presets have a damping ratio in (0, 1]. Time is in seconds.
export function sampleSpring(position, velocity, target, seconds, { stiffness, dampingRatio }) {
  const frequency = Math.sqrt(stiffness);
  const offset = position - target;
  const decay = frequency * dampingRatio;
  const envelope = Math.exp(-decay * seconds);

  if (dampingRatio === 1) {
    const slope = velocity + frequency * offset;
    return {
      position: target + envelope * (offset + slope * seconds),
      velocity: envelope * (velocity - frequency * slope * seconds),
    };
  }

  const dampedFrequency = Math.sqrt(stiffness - decay * decay);
  const angle = dampedFrequency * seconds;
  const cosine = Math.cos(angle);
  const sine = Math.sin(angle);
  const amplitude = (velocity + decay * offset) / dampedFrequency;
  const displacement = offset * cosine + amplitude * sine;
  return {
    position: target + envelope * displacement,
    velocity: envelope * (dampedFrequency * (amplitude * cosine - offset * sine) - decay * displacement),
  };
}

// For one spatial property, for example a sheet offset in CSS pixels.
export function createSpring(initial, spec, render, tolerance = 0.01) {
  const reduced = matchMedia("(prefers-reduced-motion: reduce)");
  let target = initial;
  let origin = initial;
  let initialVelocity = 0;
  let startTime = 0;
  let frame = null;

  function sample(now) {
    return sampleSpring(origin, initialVelocity, target, Math.max(0, (now - startTime) / 1000), spec);
  }

  function cancelFrame() {
    if (frame !== null) {
      cancelAnimationFrame(frame);
      frame = null;
    }
  }

  function jump(next) {
    cancelFrame();
    target = next;
    render(next);
  }

  function paint(now) {
    const state = sample(now);
    if (Math.abs(state.position - target) <= tolerance &&
        Math.abs(state.velocity) <= tolerance * Math.sqrt(spec.stiffness)) {
      frame = null;
      render(target);
      return;
    }
    render(state.position);
    frame = requestAnimationFrame(paint);
  }

  function to(next, releaseVelocity) {
    if (reduced.matches) {
      jump(next);
      return;
    }
    const now = performance.now();
    const state = frame === null ? { position: target, velocity: 0 } : sample(now);
    cancelFrame();
    origin = state.position;
    initialVelocity = releaseVelocity ?? state.velocity;
    target = next;
    startTime = now;
    frame = requestAnimationFrame(paint);
  }

  function preferenceChanged(event) {
    if (event.matches) jump(target);
  }

  reduced.addEventListener("change", preferenceChanged);
  render(initial);
  return {
    jump, to,
    dispose() {
      cancelFrame();
      reduced.removeEventListener("change", preferenceChanged);
    },
  };
}
