import React from 'react'
import Mobile from './type/mobile/main'
import Script from './type/script/main'
import Desktop from './type/desktop/main'
import Site from './type/site/main'

const info = require('./infor.json')
function main (){
        switch(info.type){
            case 'mobile':
                return <Mobile/>;
            case 'desktop':
                return <Desktop/>;
            case 'script':
                return <Script/>;
            case 'site':
                return <Site/>;
            default:
                return <Script/>
        }
}
export default function App(){
    
    return(
        <div className='App'>
            {main()}
        </div>
    )
}