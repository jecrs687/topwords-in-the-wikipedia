import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import * as serviceWorker from './serviceWorker';
const infor = require ('./infor.json')

function Title(){
    return(
        infor.title.split('_').map(value=>` ${value}`)
        )
}
function Google(){
    return(
            <div></div>
        )
}
ReactDOM.render(<App />, document.getElementById('root'));
ReactDOM.render(<Title/>, document.getElementById('title'));
ReactDOM.render(<Google/>, document.getElementById('google'));


// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
