import React from 'react'
import './script.css'
const infor = require('../../infor.json')
const colors = infor.colors

export default function main(){
    return(
        <div className='Script'>
            <div className="header" style={{background:`linear-gradient(${colors.analogo},${colors.triadic2} )`}}>
                    <div style={{backgroundColor:`${colors.triadic}`}}/>
                    <div style={{backgroundColor:`${colors.triadic}`}}/>
                    <div style={{backgroundColor:`${colors.triadic}`}}/>
                    <div style={{backgroundColor:`${colors.triadic}`}}/>

                <div className='title' style={{backgroundColor:`${colors.analogo2}88`}}>
                    <h1>
                        {infor.title.split('_').map(value=>` ${value}`)}
                    </h1>
                </div>
            </div>

            <div className="body">
                <div className='description'>
                    <h2>Description</h2>
                    <i>
                    {infor.description.map(value=><p>{value}</p>)}
                    </i>
                </div>
            </div>

            <div className="footer">
                powered by <a href='https://jecrs687.github.io' style={{color:`${colors.primary}`}}>@jecrs687</a>
            </div>

        </div>
    )
}