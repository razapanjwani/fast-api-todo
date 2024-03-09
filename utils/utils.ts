export const URL = "http://localhost:3000"
import { useRouter } from "next/router"
import { usePathname } from "next/navigation"
export const getPathName = () => {
    const pathName = usePathname()
    return pathName
}

