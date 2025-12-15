// ---------- Debounce ----------
// Runs a function only after user stops calling it for some time
function debounce(func, delay) {
  let timer; // store timer ID
  return function () {
    clearTimeout(timer); // reset timer if function called again
    timer = setTimeout(() => {
      func(); // call the function after the delay
    }, delay);
  };
}

// ---------- Throttle ----------
// Runs a function once every given time period (ignores extra calls)
function throttle(func, limit) {
  let waiting = false; // to track if waiting period is active
  return function () {
    if (!waiting) {
      func(); // run the function
      waiting = true; // block further calls
      setTimeout(() => {
        waiting = false; // allow again after limit time
      }, limit);
    }
  };
}

// ---------- groupBy ----------
// Groups items in an array based on a property (key)
function groupBy(array, key) {
  const result = {}; // object to store grouped items
  for (let item of array) {
    const group = item[key]; // value of that property
    if (!result[group]) {
      result[group] = []; // if not exist, create array
    }
    result[group].push(item); // push item into correct group
  }
  return result;
}