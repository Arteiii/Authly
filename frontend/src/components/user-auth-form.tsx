"use client";

import { ChangeEvent, useState } from "react";

import { cn } from "@/lib/utils";
import { Icons } from "@/components/icons";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useToast } from "@/components/ui/use-toast";

import React from "react";

interface UserAuthFormProps extends React.HTMLAttributes<HTMLDivElement> {}

export function UserAuthForm({ className, ...props }: UserAuthFormProps) {
  const [isLoading, setIsLoading] = React.useState<boolean>(false);
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const { toast } = useToast();
  const [isPasswordValid, setIsPasswordValid] = useState(true);
  const requirements = {
    minLength: password.length >= 8,
    hasUpperCase: /[A-Z]/.test(password),
    hasLowerCase: /[a-z]/.test(password),
    hasDigit: /\d/.test(password),
    hasSpecialChar: /[@$!%*?&]/.test(password),
  };

  const unmetRequirements = Object.entries(requirements)
    .filter(([_, condition]) => !condition)
    .map(([requirement, _]) => {
      switch (requirement) {
        case "minLength":
          return "Minimum 8 characters";
        case "hasUpperCase":
          return "At least one uppercase letter";
        case "hasLowerCase":
          return "At least one lowercase letter";
        case "hasDigit":
          return "At least one digit";
        case "hasSpecialChar":
          return "At least one special character (@, $, !, %, *, ?, &)";
        default:
          return "";
      }
    });

  const handlePasswordChange = (event: ChangeEvent<HTMLInputElement>) => {
    setPassword(event.target.value);

    const isValid =
      /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/.test(
        event.target.value
      );
    setIsPasswordValid(isValid);
    setPassword(event.target.value);
  };

  async function onSubmit(e: React.SyntheticEvent) {
    e.preventDefault();

    const data = {
      email: email,
      username: username,
      password: btoa(password), // encode the password to base64
    };

    try {
      const response = await fetch("http://localhost:8000/api/v1/user/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      const responseData = await response.json();
      console.log("reponse:", responseData);

      if ((responseData.mongo_state = true)) {
        toast({
          description: "User Created You can Continue to the login now",
        });
      } else {
        toast({
          variant: "destructive",
          title: "Uh oh! Something went wrong.",
          description: "There was a problem with your request.",
        });
        throw new Error("mongo_state is not true");
      }

      console.log("countdown start");
      setTimeout(() => {
        // Redirect to the login page
        console.log("redirecting");
        window.location.href = "/login";
      }, 5000);
    } catch (error) {
      console.error("An error occurred:", error);
    }
  }

  const data = {
    email: email,
    username: username,
    password: btoa(password), // encode the password to base64
  };

  return (
    <div className={cn("grid gap-6", className)} {...props}>
      <form onSubmit={onSubmit}>
        <div className="grid gap-2">
          <div className="grid gap-1">
            <Label className="sr-only" htmlFor="username">
              Username
            </Label>
            <Input
              id="username"
              placeholder="AuthlyAdmin"
              type="text"
              autoCapitalize="none"
              autoComplete="username"
              autoCorrect="off"
              value={username}
              disabled={isLoading}
              onChange={(e) => setUsername(e.target.value)}
            />
          </div>
          <div className="grid gap-1">
            <Label className="sr-only" htmlFor="email">
              Email
            </Label>
            <Input
              id="email"
              placeholder="name@example.com"
              type="email"
              autoCapitalize="none"
              autoComplete="email"
              autoCorrect="off"
              disabled={isLoading}
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>
          <div className="grid gap-1">
            <Label className="sr-only" htmlFor="password">
              Password
            </Label>
            <Input
              id="password"
              placeholder="S3cur€P4ss!!"
              type="password"
              autoCapitalize="none"
              autoComplete="new-password"
              autoCorrect="off"
              onChange={handlePasswordChange}
              className={isPasswordValid ? "border" : "border border-red-500"}
              disabled={isLoading}
              value={password}
            />
            {!isPasswordValid && (
              <div className="text-red-500 text-sm mt-1">
                <ul className="list-disc list-inside">
                  {unmetRequirements.map((requirement, index) => (
                    <li key={index}>{requirement}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
          <Button disabled={isLoading}>
            {isLoading && (
              <Icons.spinner className="mr-2 h-4 w-4 animate-spin" />
            )}
            Sign In with Email
          </Button>
        </div>
      </form>
      <div className="relative">
        <div className="absolute inset-0 flex items-center">
          <span className="w-full border-t" />
        </div>
        <div className="relative flex justify-center text-xs uppercase">
          <span className="bg-background px-2 text-muted-foreground">
            Or continue with
          </span>
        </div>
      </div>
      <div className="grid grid-cols-2 gap-6">
        <Button variant="outline">
          <Icons.gitHub className="mr-2 h-4 w-4" />
          Github
        </Button>
        <Button type="submit" variant="outline">
          <Icons.google className="mr-2 h-4 w-4" />
          Google
        </Button>
      </div>
    </div>
  );
}
