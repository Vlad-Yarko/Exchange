import { createContext, useState, useLayoutEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import api from "../api.js";


export const AuthContext = createContext()


export const AuthContextProvider = ({ children }) => {
    const [ bearer, setBearer ] = useState(null)
    const [ isLoading, setIsLoading ] = useState(true)
    const [ message, setMessage ] = useState({ type: '', content: '' })
    const navigate = useNavigate()
    const location = useLocation()

    useLayoutEffect(() => {
        const fetchToken = async() => {
            let accessToken = ''
            try {
                let response = await api.post('/refresh')
                let data = response.data
                accessToken = data.bearerToken
                setBearer(() => accessToken)
            } catch (error) {
                const status = error?.response?.status;
                if (status === 401 || status === 403) {
                    setBearer(null)
                    navigate('/login')
                } else {
                    setBearer(null)
                    throw new Error('API ERROR')
                }
            } finally {
                setIsLoading(false)
            }
        }
        if (!['/login', '/signup'].includes(location.pathname)) {
            fetchToken()
        }
    }, [location.pathname])

    return (
        <AuthContext.Provider value={{bearer, setBearer, message, setMessage}}>
            {children}
        </AuthContext.Provider>
    )
}
