import {createContext, useEffect, useLayoutEffect, useState} from 'react';
import { useLocation } from "react-router-dom";
import api from "../api.js";


export const BaseContext = createContext();


export const BaseContextProvider = ({ children }) => {
    const location = useLocation()

    const [ message, setMessage ] = useState({ type: '', content: '' })
    const [ tab, setTab ] = useState('/')
    const [ bearer, setBearer ] = useState(null)

    useLayoutEffect(() => {
        setTab(location.pathname)

        const fetchAccessToken = async() => {
            let accessToken = ''
            try {
                let response = await api.post('/auth/refresh')
                let data = response.data
                accessToken = data.bearerToken
                setBearer(accessToken)
            } catch (error) {
                setBearer(null)
            }
        }
        fetchAccessToken()
        let id = setInterval(() => {
            fetchAccessToken()
        }, 1000 * 60 * 12)
        return () => {
            clearInterval(id)
        }
    }, [location.pathname])

    useEffect(() => {
        const id = setTimeout(() => {
            setMessage({type: '', content: ''})
        }, 5000)

        return () => clearTimeout(id)
    }, [message])

    return (
        <BaseContext.Provider value={{ message, setMessage, tab, bearer }}>
            { children }
        </BaseContext.Provider>
    )
}
