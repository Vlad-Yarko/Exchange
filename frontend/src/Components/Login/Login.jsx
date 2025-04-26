import { useContext, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import AuthFormLayout from "../AuthFormLayout/AuthFormLayout.jsx";
import { AuthFormContext } from "../../Context/AuthFormContext.jsx";
import api from "../../api.js";
import { AuthContext } from "../../Context/AuthContext.jsx";


function Login() {
    const navigate = useNavigate()

    const { setUsername, setPassword, password, username, passwordValidate, usernameValidate } = useContext(AuthFormContext)
    const { setMessage } = useContext(AuthContext)

    useEffect(() => {
        document.title = 'AUTH login'
    }, [])

    function handleSubmit(event) {
        event.preventDefault()
        const p = passwordValidate(password)
        const u = usernameValidate(username)
        setUsername('')
        setPassword('')
        const fetchApi = async() => {
            if (!p && !u) {
                const form = event.target
                const formData = new FormData(form)
                try {
                    const response = await api.post('/login', formData, {
                        headers: {
                            'Content-Type': 'multipart/form-data'
                        }
                    })
                    setMessage({type: 'message', content: 'You logged in successfully'})
                    navigate('/')
                } catch (error) {
                    const status = error.response.status
                    if (status === 409) {
                        setMessage({type: 'error', content: 'You are already logged in'})
                        navigate('/')
                    } else if (status === 422) {
                        setMessage({type: 'error', content: error.response.data.message})
                    }
                }
            } else {
                setMessage({type: 'error', content: 'Incorrect credentials'})
            }
        }
        fetchApi()
    }

    return (
        <AuthFormLayout
            label='Sing up'
            to='/signup'
            act='Log in'
            handleSubmit={handleSubmit}
        />
    )
}


export default Login
