// This file is concatenated to the beginning of every output.
// It defines the top-level runtime environment with modules.
// Maybe in the future it will be written entirely in python.
(function (root) {

  // the root boa object
  var boa = root.boa$ = {};

  // the boa prelude(provided to every module)
  var prelude = boa.prelude = {};

  // a 'registry' of sorts for modules
  // the paths are strings that look like this:
  // my.module => my/module/__init__.py
  // my.module.x => my/module/x.py
  // my => my/__init__.py
  // the values are modules that have been generated with boa.mod, module objects
  var modules = boa.modules = {};

  // the import function to be used with a module
  // takes a path for the module that will do the importing, as well as its imports$ object
  var imp = boa.imp = function (importer) {

    var path = importer.split('.');

    // takes the object to be imported into,
    // module to be imported, and names (if they are specified)
    // import my_module => import(module, 'my_module')
    // from my_module import a, b => import(module, 'my_module', ['a', 'b'])
    // from my_module import * => import(module, 'my_module', 'all')
    return function (object, importee, names) {

      // relative imports not yet
      if(importee.charAt(0) == '.') {
        throw new Error('relative imports are not supported for now');
      }

      if(importee.contains('.')) {
        var importee_path = importee.split('.');
      } else {

      }

    };
  };

  // class for modules, takes code function
  var Module = boa.Module = function (path, code) {
    this.path = path;
    this.code = code;
    this.value = null;
    this.loaded = false;
  };

  // Load this module
  Module.prototype.load = function () {
    if(!this.loaded) {

      var module = {};
      prelude.import = imp(this.path);

      this.code(module, prelude);
      this.value = module;
    }
    return this.value;
  };

  // class for packages, takes code function
  var Package = boa.Package = function (code) {

  };

  // Define a module.
  // calls to this are generated by the code generator, they look like this:
  // boa$.mod('my.module.x', function (module$, prelude$) {});
  // or definining an __init__.py
  // boa$.mod('my.module.__init__', function (module$, prelude$) {});
  var mod = boa.mod = function (path, code) {
    boa.modules[path] = new Module(path, code);
  };

  // set the main value
  var main = boa.main = function (path) {
    boa.__main__ = path;
  };

  // also called by generator, like this:
  // boa$.start();
  var start = boa.start = function () {
    boa.modules[boa.__main__].load();
  };

})(this);