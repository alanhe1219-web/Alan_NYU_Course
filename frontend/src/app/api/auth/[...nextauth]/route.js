import NextAuth from "next-auth";
import CredentialsProvider from "next-auth/providers/credentials";

const authOptions = {
    providers: [
        CredentialsProvider({
            name: "NYU Email",
            credentials: {
                email: { label: "NYU Email", type: "email", placeholder: "netid@nyu.edu" }
            },
            async authorize(credentials) {
                if (credentials?.email && credentials.email.endsWith("@nyu.edu")) {
                    return { id: credentials.email, email: credentials.email, name: credentials.email.split("@")[0] };
                }
                return null;
            }
        })
    ],
    pages: {
        signIn: '/login',
    },
    session: {
        strategy: "jwt",
    },
    callbacks: {
        async session({ session, token }) {
            if (session?.user && token?.sub) {
                session.user.id = token.sub;
            }
            return session;
        },
    }
};

const handler = NextAuth(authOptions);

export { handler as GET, handler as POST };
