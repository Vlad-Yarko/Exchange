import { useEffect, useContext } from "react";
import { BaseContext } from "../../../Context/BaseContext.jsx";
import { AuthFormContext } from "../../../Context/AuthFormContext.jsx";
import Google from "../../elements/Google/Google.jsx";
import AuthFormButton from "../../elements/AuthFormButton/AuthFormButton.jsx";


function AuthFormLayout({ handleSubmit, to, label, content, act }) {
    const { setUsername, setPassword, password, username, passwordValidate, usernameValidate, setUsernameError, setPasswordError, usernameError, passwordError } = useContext(AuthFormContext)
    const { message, setMessage } = useContext(BaseContext)

    const changeUsername = (event) => {
        setUsername(event.target.value)
    }

    const changePassword = (event) => {
        setPassword(event.target.value)
    }

    useEffect(() => {
        const error = usernameValidate(username)
        setUsernameError(error)
    }, [username])

    useEffect(() => {
        const error = passwordValidate(password)
        setPasswordError(error)
    }, [password])

    return (
        <>
            <h1 className={`min-h-[60px] text-[40px] text-${message.type === 'error' ? 'red' : 'green'}-500 text-center`}>{message.content}</h1>
            <div className='text-center flex items-center justify-center'>
                <form
                    className='bg-yellow-50 mt-30 w-1/2 text-amber-600 text-[200%] p-9 border-4 rounded-[20px] border-amber-600 pb-30'
                    onSubmit={handleSubmit}>
                    <label htmlFor='username'>Username</label>
                    <input id='username' name='username' type='text' onChange={changeUsername} value={username}
                           className='border-2 rounded-[20px] p-4 bg-emerald-300'/><br/>
                    <h1 className='min-h-[30px] text-[20px] text-red-500'>{usernameError}</h1>
                    <label htmlFor='password'>Password</label>
                    <input id='password' name='password' type='password' onChange={changePassword} value={password}
                           className='border-2 rounded-[20px] p-4 bg-emerald-300'/><br/>
                    <h1 className='min-h-[30px] text-[20px] text-red-500'>{passwordError}</h1>
                    <button type='submit' className='mb-10 mt-20 bord er-2 rounded-[20px] p-4 bg-emerald-300'>{act}
                    </button>
                    <AuthFormButton content={content} to={to} label={label}/>
                    <Google />
                </form>
            </div>
        </>
    )
}

export default AuthFormLayout
