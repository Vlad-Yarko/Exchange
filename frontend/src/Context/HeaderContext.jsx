import React, {createContext, useState, useEffect} from 'react';
import { useLocation } from "react-router-dom";
import api from "../api.js";

export const HeaderContext = createContext();

export const HeaderContextProvider = ({ children }) => {
    const location = useLocation()
    const [ tab, setTab ] = useState('/')
    const [ bearer, setBearer ] = useState(null)

    useEffect(() => {
        setTab(location.pathname)
    }, [location.pathname])

    return (
        <HeaderContext value={{ tab, setTab }}>
            {children}
        </HeaderContext>
    )
}