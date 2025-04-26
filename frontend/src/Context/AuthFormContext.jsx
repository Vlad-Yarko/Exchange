import { createContext, useState, useEffect } from "react";

export const AuthFormContext = createContext({
    username: '',
    setUsername: () => {},
    password: '',
    setPassword: () => {},
    usernameError: '',
    setUsernameError: () => {},
    passwordError: '',
    setPasswordError: () => {},
    usernameValidate: () => '',
    passwordValidate: () => '',
})


export const AuthFormContextProvider = ({ children }) => {

    const [ username, setUsername ] = useState('')
    const [ password, setPassword ] = useState('')
    const [ usernameError, setUsernameError ] = useState('')
    const [ passwordError, setPasswordError ] = useState('')

    const usernameValidate = (u) => {
        if (u.length < 2 || u.length > 25) {
            return 'Username must be between 2 and 25 characters'
        }
        if ([' ', '!', '?', '<', '>', '.', '/', '\\', '|', ':', ';', '`', '~', '!', '@', '#', "&"]
            .some(element => u.includes(element))) {
            return 'Username must contain only characters or numbers'
        }
        return ''
    }

    const passwordValidate = (p) => {
        if (p.length < 8 || p.length > 50) {
            return 'Password must be between 8 and 50 characters'
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
            usernameValidate,
            passwordValidate}}>
            {children}
        </AuthFormContext.Provider>
    )
}
