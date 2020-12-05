const callback = () => {
  const stepper = document.getElementById('stepper');
  const increaseBtn = stepper.nextElementSibling;
  const decreaseBtn = stepper.previousElementSibling;
  const max = parseInt(stepper.max);
  const min = parseInt(stepper.min);

  increaseBtn.addEventListener('click', () => {
    let curr = parseInt(stepper.value);
    if (curr < max) {
      curr += 1;
      stepper.value = curr;
    }
    if (curr >= max) {
      increaseBtn.setAttribute('disabled', true);
    }
    if (curr > min) {
      decreaseBtn.removeAttribute('disabled');
    }
  });
  decreaseBtn.addEventListener('click', () => {
    let curr = parseInt(stepper.value);
    if (curr > min) {
      curr -= 1;
      stepper.value = curr;
    }
    if (curr <= min) {
      decreaseBtn.setAttribute('disabled', true);
    }
    if (parseInt(stepper.value) < max) {
      increaseBtn.removeAttribute('disabled');
    }
  });
};

if (
  document.readyState === 'complete' ||
  (document.readyState !== 'loading' && !document.documentElement.doScroll)
) {
  callback();
} else {
  window.addEventListener('DOMContentLoaded', callback);
}
