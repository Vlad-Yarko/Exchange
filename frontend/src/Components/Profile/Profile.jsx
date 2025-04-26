import { useContext, useEffect, useState } from 'react'
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../../Context/AuthContext.jsx";
import api from "../../api.js";

function Profile() {
    const navigate = useNavigate()

    const { bearer, setMessage, isLoading } = useContext(AuthContext)
    const [ username, setUsername ] = useState('')

    useEffect(() => {

        if (!bearer) {
            return
        }

        document.title = 'AUTH Profile'
        const fetchUserData = async() => {
            try {
                const response = await api.get('/username', {
                    headers: {
                        Authorization: `Bearer ${bearer}`
                    }
                })
                const data = response.data
                setUsername(data?.username)
            } catch (error) {
                const response = error.response
                const status = response.status
                if (status === 401) {
                    setMessage({type: 'error', content: 'You are not logged in'})
                    navigate('/login')
                }
            }
        }
        fetchUserData()
    }, [bearer])

    return (
        <div className='h-screen flex justify-center items-center'>
            <h1 className='text-amber-600 text-[200%] p-9 border-4 rounded-[20px] border-amber-600'>
                Username: {username}
            </h1>
        </div>
    )
}


export default Profile
