import {createContext, useState, useEffect, useContext} from 'react';
import { useNavigate, useLocation } from "react-router-dom";
import api from '../api.js'
import { BaseContext } from "./BaseContext.jsx";


export const ProtectedContext = createContext();


export const ProtectedContextProvider = ({ children }) => {
    const { setMessage, bearer } = useContext(BaseContext)
    const [ username, setUsername ] = useState('')
    const [ email, setEmail ] = useState('')
    const [ logoutClicked, setLogoutClicked ] = useState(false)


    const navigate = useNavigate()
    const location = useLocation()


    useEffect(() => {
        if (!bearer) {
            setMessage({ type: 'error', content: "You are not logged in" })
            navigate('/auth/login')
        }

    }, [location.pathname])


    return (
        <ProtectedContext.Provider value={{username, setMessage, email, setEmail, logoutClicked, setLogoutClicked}}>
            { children }
        </ProtectedContext.Provider>
    )
}
