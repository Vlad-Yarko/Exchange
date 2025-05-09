import { Outlet, useLocation, useNavigate } from "react-router-dom";
// import { AuthContextProvider } from '../../../Context/AuthContext.jsx'
import { useContext, useLayoutEffect } from "react";
import { BaseContext } from "../../../Context/BaseContext.jsx";
import api from "../../../api.js";


function AuthMiddleware() {
    const { setMessage } = useContext(BaseContext)

    const navigate = useNavigate()


    useLayoutEffect(() => {
        const isLoggedIn = async() => {
            let response = await api.post('/auth/is-logged-in')
            let data = response.data
            let message = data.message
            if (message) {
                setMessage({type: 'error', content: 'You are logged in'})
                navigate('/')
            }
        }
        isLoggedIn()
    }, [])


    return (
        <>
            {/*<AuthContextProvider>*/}
                <Outlet />
            {/*</AuthContextProvider>*/}
        </>
    )
}


export default AuthMiddleware
