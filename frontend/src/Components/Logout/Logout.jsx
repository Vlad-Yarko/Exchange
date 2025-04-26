import { useEffect, useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import api from "../../api.js";
import { AuthContext } from "../../Context/AuthContext.jsx";

function Logout() {
    const navigate = useNavigate()
    const { setMessage } = useContext(AuthContext)

    useEffect(() => {
        document.title = 'AUTH logout'
    }, [])

    function handleLogout() {
        const logoutRequest = async() => {
            try {
                const response = await api.post('/logout')
                const data = response.data
                const apiMessage = data.message
                setMessage({type: 'message', content: apiMessage})
            } catch (error) {
                const response = error.response
                const status = response.status
                if (status === 401) {
                    const apiMessage = response.data.message
                    setMessage({type: 'error', content: apiMessage})
                }
            }
            navigate('/login')
        }
        logoutRequest()
    }

    return (
        <div className='flex flex-col items-center justify-center'>
            <h1 className='text-[40px] text-rose-500 mt-30'>Do you really want to logout from your account?</h1>
            <button type='submit' className='mb-10 mt-10 bord er-2 rounded-[20px] p-4 bg-rose-600 w-1/2 py-6 text-yellow-500 text-[20px]' onClick={handleLogout}>
                Log out
            </button>
        </div>
    )
}


export default Logout
