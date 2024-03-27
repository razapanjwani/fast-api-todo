"use client"
import Link from "next/link"
import Image from "next/image"
import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import { URL } from "@/utils/utils"
import { mySetCookie } from "@/utils/authhelper"
import ErrorBlock from "../component/errorblock"
const LoginPage = () => {
    const router = useRouter()
    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")
    const [loginError, setLoginError] = useState("")
    const logIn = async () => {
        const formData = new URLSearchParams();

        formData.append('username', username);
        formData.append('password', password);
        try {
            const res = await fetch(`${URL}/api/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: formData
            })

            const data = await res.json()
            if (data && data.access_token && data.refresh_token) {
                await mySetCookie(data.access_token, data.refresh_token)
                router.refresh()
                router.push("/")
                setLoginError("")
            }
            console.log(data, "datajson");
            if (res.status == 401) {
                setLoginError(data.detail)
            }
        }
        catch (error) {
            console.log(error.message, "error");
            console.log("error is error");
        }
    }
    return (
        <>
            <section className="bg-gray-50 dark:bg-gray-900 relative">
                <div className="flex flex-col items-center justify-center px-6 py-8 mx-auto  ">

                    <div className="w-full bg-white rounded-lg shadow dark:border md:mt-0 sm:max-w-md xl:p-0 dark:bg-gray-800 dark:border-gray-700">
                        <div className="p-6 space-y-4 md:space-y-6 sm:p-8">
                            <h1 className="text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl dark:text-white">
                                Log in to your account
                            </h1>
                            <form className="space-y-4 md:space-y-6" action="#" onSubmit={(e) => { e.preventDefault(); logIn() }}>
                                <div>
                                    <label htmlFor="username" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Your username</label>
                                    <input type="text" value={username} onChange={(e) => { setUsername(e.target.value) }} name="username" id="username" className="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="john doe" required={true} />
                                </div>
                                <div>
                                    <label htmlFor="password" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Password</label>
                                    <input type="password" value={password} onChange={(e) => { setPassword(e.target.value) }} name="password" id="password" placeholder="••••••••" className="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" required={true} />
                                </div>
                                <button type="submit" className="w-full text-black bg-primary-600 hover:bg-primary-700 focus:ring-4 focus:outline-none focus:ring-primary-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-primary-600 dark:hover:bg-primary-700 dark:focus:ring-primary-800">Log in</button>
                                <p className="text-sm font-light text-gray-500 dark:text-gray-400">
                                    Don’t have an account yet? <Link href="/signup" className="font-medium text-primary-600 hover:underline dark:text-primary-500">Sign up</Link>
                                </p>
                                {loginError && <ErrorBlock error={loginError} />}
                            </form>
                        </div>
                    </div>
                </div>
            </section>
        </>
    )
}
export default LoginPage