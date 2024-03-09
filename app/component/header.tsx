"use client"
import Image from "next/image"
import Link from "next/link"
import Logo from "@/public/logo.png"
import { useEffect } from "react"
import { useRouter } from "next/navigation"
import { getPathName } from "../../utils/utils"
import { URL } from "../../utils/utils"
import { myDelCookie } from "../../utils/authhelper"
const Header = () => {
    const router = useRouter()
    const pathName = getPathName()

    const delCookie = async () => {
        myDelCookie()
        router.refresh()
    }

    return (
        <>
            <header className="my-4">
                <div className="flex justify-between items-center mx-3 md:mx-0">
                    <Link href={"/"}><Image src={Logo} alt="Todo app logo" width={100} height={100}></Image></Link>
                    <nav>
                        <ul className="inline-flex md:space-x-10 space-x-5 font-medium text-base md:text-xl font-mono">
                            <li><Link href={"/login"} onClick={() => {
                                if (pathName == "/login") {
                                    return
                                } else {
                                    delCookie()
                                }
                            }}>{pathName == "/" ? "Logout" : "Login"}</Link></li>
                            <li><Link href={"/signup"}>Signup</Link></li>

                        </ul>
                    </nav>
                </div>
            </header>
        </>
    )
}
export default Header