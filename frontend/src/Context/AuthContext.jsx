// import { createContext, useState, useLayoutEffect, useContext } from 'react';
// import { useNavigate, useLocation } from "react-router-dom";
// import api from '../api.js'
// import { BaseContext } from "./BaseContext.jsx";
//
//
// export const AuthContext = createContext();
//
//
// export const AuthContextProvider = ({ children }) => {
//     const { setMessage } = useContext(BaseContext)
//
//     const navigate = useNavigate()
//     const location = useLocation()
//
//
//     useLayoutEffect(() => {
//         const isLoggedIn = async() => {
//             let response = await api.post('/auth/is-logged-in')
//             let data = response.data
//             let message = data.message
//             if (message) {
//                 setMessage({type: 'error', content: 'You are logged in'})
//                 navigate('/')
//             }
//         }
//         isLoggedIn()
//     }, [location.pathname])
//
//
//     return (
//         <AuthContext value={}>
//             { children }
//         </AuthContext>
//     )
// }
