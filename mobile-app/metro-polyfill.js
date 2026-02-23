// Polyfills for Node.js < 18.14.0
const os = require('os');

// Polyfill os.availableParallelism
if (!os.availableParallelism) {
  os.availableParallelism = () => os.cpus().length;
}

// Polyfill Array.prototype.toReversed (ES2023 feature)
if (!Array.prototype.toReversed) {
  Array.prototype.toReversed = function() {
    return [...this].reverse();
  };
}

// Polyfill Array.prototype.toSorted (ES2023 feature)
if (!Array.prototype.toSorted) {
  Array.prototype.toSorted = function(compareFn) {
    return [...this].sort(compareFn);
  };
}

// Polyfill Array.prototype.toSpliced (ES2023 feature)
if (!Array.prototype.toSpliced) {
  Array.prototype.toSpliced = function(start, deleteCount, ...items) {
    const copy = [...this];
    copy.splice(start, deleteCount, ...items);
    return copy;
  };
}
