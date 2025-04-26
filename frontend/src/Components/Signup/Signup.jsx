import { useContext, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import AuthFormLayout from "../AuthFormLayout/AuthFormLayout.jsx";
import { AuthFormContext } from "../../Context/AuthFormContext.jsx";
import api from "../../api.js";
import { AuthContext } from "../../Context/AuthContext.jsx";

function Signup() {
    const navigate = useNavigate()

    const { setUsername, setPassword, password, username, passwordValidate, usernameValidate } = useContext(AuthFormContext)
    const { setMessage } = useContext(AuthContext)

    useEffect(() => {
        document.title = 'AUTH Sing Up'
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
                    const response = await api.post('/signup', formData, {
                        headers: {
                            'Content-Type': 'multipart/form-data'
                        }
                    })
                    setMessage({type: 'message', content: 'You created account successfully'})
                    navigate('/login')
                } catch (error) {
                    const status = error.response.status
                    if (status === 422) {
                        const errorMessage = error.response.data.message
                        setMessage({type: 'error', content: errorMessage})
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
            label='Log in'
            to='/login'
            act='Sign up'
            handleSubmit={handleSubmit}
        />
    )
}


export default Signup
