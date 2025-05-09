import { useEffect, useState, useContext } from 'react'
import HeaderElement from "../HeaderElement/HeaderElement.jsx";
import { BaseContext } from "../../../Context/BaseContext.jsx";


function Header() {
    const { bearer } = useContext(BaseContext)

    return (
        <>
            <nav className={'bg-amber-300 py-8'}>
                <ul className='flex justify-evenly text-[150%] text-amber-700'>
                    <HeaderElement link='/' label='Home' links={['/']} />
                    {bearer
                        ? <HeaderElement link='/account/me' label={`Account`} links={['/account/me']}/>
                        : <HeaderElement link={`/auth/login`} label={`Login`} links={['/auth/login', '/auth/signup']}/>
                    }
                </ul>
            </nav>
        </>
    )
}


export default Header
