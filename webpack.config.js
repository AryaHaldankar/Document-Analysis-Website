import path from 'path';
import HtmlWebpackPlugin from 'html-webpack-plugin';
import { fileURLToPath } from 'url';
import Dotenv from 'dotenv-webpack';

export default { 
  entry: './index.js', // your app's entry point
  output: {
    filename: 'bundle.js',
    path: path.resolve('dist'),
    clean: true,
  },
  mode: 'development',
  devServer: {
    static: './dist',
    open: true,
    port: 8080,
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: './index.html', // base HTML to use
    }),
    new Dotenv()
  ],
  module: {
    rules: [
      {
        test: /\.css$/i,
        use: ['style-loader', 'css-loader'],
      },
    ],
  },
};
