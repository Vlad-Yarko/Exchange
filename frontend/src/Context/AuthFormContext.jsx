import { createContext, useEffect, useState } from 'react';
import { useLocation } from "react-router-dom";
import api from "../api.js";


export const AuthFormContext = createContext();


export const AuthFormContextProvider = ({ children }) => {

    const [ username, setUsername ] = useState('')
    const [ password, setPassword ] = useState('')
    const [ usernameError, setUsernameError ] = useState('')
    const [ passwordError, setPasswordError ] = useState('')

    const usernameValidate = (u) => {
        if (u.length < 3 || u.length > 40) {
            return 'Username must be between 3 and 40 characters'
        }
        if ([' ', '!', '?', '<', '>', '.', '/', '\\', '|', ':', ';', '`', '~', '!', '@', '#', "&"]
            .some(element => u.includes(element))) {
            return 'Username must contain only characters or numbers'
        }
        return ''
    }

    const passwordValidate = (p) => {
        if (p.length < 8 || p.length > 70) {
            return 'Password must be between 8 and 70 characters'
        }
        return ''
    }

    return (
        <AuthFormContext.Provider value={{
            username,
            setUsername,
            password,
            setPassword,
            usernameError,
            setUsernameError,
            passwordError,
            setPasswordError,
            passwordValidate,
            usernameValidate
        }}>
            { children }
        </AuthFormContext.Provider>
    )
}
