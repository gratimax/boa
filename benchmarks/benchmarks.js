var Benchmark = require('benchmark');

var propAccess = new Benchmark.Suite('prop-access');

var o = {
  myFn: function () {
    return 1 + 2;
  },
  __getattr__: function (key) {
    return this[key];
  },
  $_getmyFn: function () {
    var $t1$;
    if($t1$ = this.myFn) {
      return $t1$;
    } else {
      return this.__getattr__('myFn');
    }
  },
  myFnCall: {
    __call__: function () {
      return 1 + 2;
    },
    __getattr__: function (key) {
      return this[key];
    }
  }
};

propAccess
  .add('plain', function () {
    o.myFn();
  }).add('__getattr__', function () {
    o.__getattr__('myFn')();
  }).add('__call__', function () {
    o.myFnCall.__call__();
  }).add('__getattr__ + __call__', function () {
    o.__getattr__('myFnCall').__call__();
  }).add('__getattr__ + __call__ + __getattr__', function () {
    o.__getattr__('myFnCall').__getattr__('__call__')();
  }).add('check', function () {
    if(o.__getattr__) {
      o.__getattr__('myFn')();
    } else {

    }
  }).add('checkAttr + __call__', function () {
    if(o.myFnCall) {
      o.myFnCall.__call__();
    } else {

    }
    var $t1$;
    //(($t1$ = ($t1$ = (($t1$ = o).__getattr__ ? ($t1$.__getattr__('a')) : ($t1$.a))).__getattr__ ? ($t1$.__getattr__('b')) : ($t1$.ab)).__getattr__ ? ($t1.__getattr__('__call__')) : $t1$.__call__)()
  }).add('fn', function () {
    o.$_getmyFn()();
  }).on('cycle', function (evt) {
    console.log(evt.target);
  }).on('complete', function () {
    console.log(this.map(function (test) {
      return {name: test.name, hz: test.hz};
    }));
  })
  .run({ 'async': true  });
