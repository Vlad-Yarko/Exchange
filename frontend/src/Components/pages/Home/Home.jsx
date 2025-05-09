import { useEffect, useContext } from "react";


function Home() {

    useEffect(() => {
        document.title = 'E home'
    }, [])

    return (
        <>
            {/*<h1 className={`min-h-[60px] text-[40px] text-${message.type === 'error' ? 'red' : 'green'}-500 text-center`}>{message.content}</h1>*/}
            {/*<div className='h-screen flex justify-center items-center'>*/}
            {/*    <h1 className='text-amber-600 text-[200%] p-9 border-4 rounded-[20px] border-amber-600'>*/}
            {/*        AUTH HOME*/}
            {/*    </h1>*/}
            {/*</div>*/}
            <h1>Home</h1>
        </>
    )
}


export default Home
