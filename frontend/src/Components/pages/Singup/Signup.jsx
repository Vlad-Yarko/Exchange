import {useContext, useEffect} from "react";
import AuthFormLayout from "../../layouts/AuthFormLayout/AuthFormLayout.jsx";
import { BaseContext } from "../../../Context/BaseContext.jsx";
import { AuthFormContext } from "../../../Context/AuthFormContext.jsx";
import api from "../../../api.js";


function Signup() {
    const { setUsername, setPassword, password, username, passwordValidate, usernameValidate } = useContext(AuthFormContext)
    const { setMessage } = useContext(BaseContext)

    useEffect(() => {
        document.title = 'E signup'
    }, [])

    function handleSubmit(event) {
        event.preventDefault()
        const p = passwordValidate(password)
        const u = usernameValidate(username)
        const fetchApi = async() => {
            if (!p && !u) {
                const form = event.target
                const formData = new FormData(form)
                try {
                    const response = await api.post('/auth/signup', formData, {
                        headers: {
                            'Content-Type': 'multipart/form-data'
                        }
                    })
                    data = response.data
                    setMessage({type: 'message', content: data.message})
                    navigate('/auth/login')
                } catch (error) {
                    const status = error.response.status
                    if (status === 403) {
                        setMessage({type: 'error', content: error.response.data.message})
                        navigate('/')
                    } else if (status === 422) {
                        setMessage({type: 'error', content: error.response.data.message})
                    }
                }
            } else {
                setMessage({type: 'error', content: 'Incorrect credentials'})
            }
            setUsername('')
            setPassword('')
        }
        fetchApi()
    }

    return (
        <>
            <AuthFormLayout
                handleSubmit={handleSubmit}
                content={`Already`}
                label={`Log in`}
                act={`Sign up`}
                to={`/auth/login`}
            />
        </>
    )
}

export default Signup
