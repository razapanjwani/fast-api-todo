"use client"
import Image from "next/image";
import Link from "next/link";
import Todo from "./component/todo";
import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { myGetCookie } from "../utils/authhelper";

export default function Home() {
  const router = useRouter()
  const redirection = async () => {
    const cookies = await myGetCookie()
    if (!cookies.access_token && !cookies.refresh_token) {
      router.push("/login")
      return cookies
    }
  }
  useEffect(() => {
    redirection()
  })
  return (
    <div>
      <Todo />
    </div>
  );
}
