import { useEffect, useState } from 'react'
import HeaderElement from "../HeaderElement/HeaderElement.jsx";
import { HeaderContextProvider } from "../../Context/HeaderContext.jsx";
import api from "../../api.js";

function Header() {
    const [ bearer, setBearer ] = useState('')

    useEffect(() => {
        const fetchToken = async() => {
            try {
                let response = await api.post('/refresh')
                let data = response.data
                let accessToken = data.bearerToken
                setBearer(() => accessToken)
            } catch (error) {}
        }
        fetchToken()
    }, [])

    return (
        <>
            <nav className={'bg-amber-300 py-8'}>
                <ul className='flex justify-evenly text-[150%] text-amber-700'>
                    <HeaderContextProvider>
                        <HeaderElement link='/' label='Home'/>
                        {bearer
                            ? <><HeaderElement link='/logout' label='Logout'/>
                                <HeaderElement link='/me' label='Profile'/></>
                            : <><HeaderElement link='/login' label='Login'/>
                                <HeaderElement link='/signup' label='Signup'/></>
                        }
                    </HeaderContextProvider>
                </ul>
            </nav>
        </>
    )
}


export default Header
