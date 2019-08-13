var path = require('path');
var webpack = require('webpack');
var HtmlWebpackPlugin = require('html-webpack-plugin');
var CleanWebpackPlugin = require('clean-webpack-plugin');
var CopyWebpackPlugin = require('copy-webpack-plugin');

module.exports = {
  entry: './src/main.js',
  output: {
    path: path.resolve(__dirname, './dist'),
    filename: process.env.NODE_ENV === 'development'? 'bundle.js' :'build.[hash:6].js',
    // 下面属性用来规定打包后的主文件(build.js)加载懒加载文件(0.build.js)的调用路径
    publicPath: process.env.NODE_ENV === 'production' ? './static/' : '/dist/'
  },
  module: {
    rules: [
      {
        test: /\.css$/,
        use: [
          'vue-style-loader',
          'css-loader'
        ],
      },
      {
        test: /\.scss$/,
        use: [
          'vue-style-loader',
          'css-loader',
          'sass-loader'
        ],
      },
      {
        test: /\.sass$/,
        use: [
          'vue-style-loader',
          'css-loader',
          'sass-loader?indentedSyntax'
        ],
      },
      {
        test: /\.vue$/,
        loader: 'vue-loader',
        options: {
          loaders: {
            // Since sass-loader (weirdly) has SCSS as its default parse mode, we map
            // the "scss" and "sass" values for the lang attribute to the right configs here.
            // other preprocessors should work out of the box, no loader config like this necessary.
            'scss': [
              'vue-style-loader',
              'css-loader',
              'sass-loader'
            ],
            'sass': [
              'vue-style-loader',
              'css-loader',
              'sass-loader?indentedSyntax'
            ]
          }
          // other vue-loader options go here
        }
      },
      {
        test: /\.js$/,
        loader: 'babel-loader',
        exclude: /node_modules/
      },
      {
        test: /\.(png|jpg|gif|svg|ttf|woff)$/,
        // 原来file-loader会导致element-ui的icon无法显示
        loader: 'url-loader',
        options: {
          name: '[name].[ext]?[hash]'
        }
      }
    ]
  },
  resolve: {
    alias: {
      'vue$': 'vue/dist/vue.esm.js',
      '@': path.resolve(__dirname, 'src')
    },
    extensions: ['*', '.js', '.vue', '.json']
  },
  devServer: {
    historyApiFallback: true,
    noInfo: true,
    overlay: true,
    // contentBase: './'
    watchContentBase: true,
    proxy: {
      "/api": {
        target: "http://localhost:5000"
      }
    }

  },
  performance: {
    hints: false
  },
  devtool: '#eval-source-map',
  plugins: [
    new HtmlWebpackPlugin({
      template: process.env.NODE_ENV === 'production' ? './src/index.html' : './index.html',
      filename: 'index.html',
    }),
    new CleanWebpackPlugin({
      // cleanOnceBeforeBuildPatterns: ['./*', '!./assets'],
    }),
    new CopyWebpackPlugin([
      {from: './src/assets/', to: './assets/'}
    ])

  ]
};

if (process.env.NODE_ENV === 'production') {
  module.exports.devtool = '';
  // http://vue-loader.vuejs.org/en/workflow/production.html
  module.exports.plugins = (module.exports.plugins || []).concat([
    new webpack.DefinePlugin({
      'process.env': {
        NODE_ENV: '"production"'
      }
    }),
    new webpack.optimize.UglifyJsPlugin({
      sourceMap: false,
      compress: {
        warnings: false
      }
    }),
    new webpack.LoaderOptionsPlugin({
      minimize: true
    })
  ])
}
