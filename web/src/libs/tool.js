function scroll (toHeight, time, mode=1) {
  // 滚动的细分次数，
  // 实测发现滚动一次需要大约4ms时间，因此time小于400就没有意义了。
  var pieces = 100;

  var fromHeight = document.documentElement.scrollTop;
  var interval = time / pieces;
  var distance = toHeight - fromHeight
  var stepLength = distance / pieces;

  if (mode === 0) {
    // linear
    var scrollTimer = window.setInterval(function () {
      var curHeight = document.documentElement.scrollTop;
      if ((stepLength >=0 && curHeight < toHeight) ||
          (stepLength <0 && curHeight > toHeight))  {
        document.documentElement.scrollTop = curHeight + stepLength;
      } else {
        window.clearInterval(scrollTimer);
      }
      if (document.documentElement.scrollTop === curHeight) {
        // 已经滚到无法滚动了，必须终止
        window.clearInterval(scrollTimer);
      }
    }, interval);
  } else {
    // ease
    var count = 0;

    var scrollTimer = window.setInterval(function () {
      stepLength = (Math.cos(count++ * Math.PI / pieces) - 1) * distance / -2;
      document.documentElement.scrollTop = fromHeight + stepLength;
      if (count > pieces) {
        window.clearInterval(scrollTimer);
      }
    }, interval);
  }
}

export default {
  scroll: scroll
}
