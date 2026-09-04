const path = require('path');

module.exports = {
  mode: process.env.NODE_ENV === 'development' ? 'development' : 'production',
  entry: './index.js',
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'bundle.js',
    library: {
      name: 'ImmunoStudy',
      type: 'umd',
      export: 'default',
    },
    globalObject: 'this',
    clean: true,
  },
  devtool: process.env.NODE_ENV === 'development' ? 'source-map' : false,
};
