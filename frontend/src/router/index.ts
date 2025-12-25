import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/apartments',
    name: 'apartments',
    component: () => import('../views/ApartmentsView.vue')
  },
  {
    path: '/apartments/:id',
    name: 'apartmentDetail',
    component: () => import('../views/ApartmentDetailView.vue')
  },
  {
    path: '/search',
    name: 'search',
    component: () => import('../views/SearchView.vue')
  },
  {
    path: '/put-an-ad',
    name: 'putAnAd',
    component: () => import('../views/PutAnAdView.vue'),
    meta: { requiresAuth: true, requiresRenter: true }
  },
  {
    path: '/my-apartments',
    name: 'myApartments',
    component: () => import('../views/MyApartmentsView.vue'),
    meta: { requiresAuth: true, requiresRenter: true }
  },
  {
    path: '/my-apartments/:id/edit',
    name: 'editApartment',
    component: () => import('../views/EditApartmentView.vue'),
    meta: { requiresAuth: true, requiresRenter: true }
  },
  {
    path: '/messages',
    name: 'messages',
    component: () => import('../views/MessagesView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/messages/:userId',
    name: 'conversation',
    component: () => import('../views/ConversationView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/notifications',
    name: 'notifications',
    component: () => import('../views/NotificationsView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/profile',
    name: 'profile',
    component: () => import('../views/ProfileView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/admin',
    name: 'admin',
    component: () => import('../views/admin/AdminDashboard.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/users',
    name: 'adminUsers',
    component: () => import('../views/admin/UsersManagement.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/about',
    name: 'about',
    component: () => import('../views/AboutView.vue')
  },
  {
    path: '/contact',
    name: 'contact',
    component: () => import('../views/ContactView.vue')
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('../views/auth/LoginView.vue'),
    meta: { guestOnly: true }
  },
  {
    path: '/signup',
    name: 'signup',
    component: () => import('../views/auth/SignUpView.vue'),
    meta: { guestOnly: true }
  },
  {
    path: '/forgot-password',
    name: 'forgotPassword',
    component: () => import('../views/auth/ForgotPasswordView.vue'),
    meta: { guestOnly: true }
  },
  {
    path: '/reset-password',
    name: 'resetPassword',
    component: () => import('../views/auth/ResetPasswordView.vue'),
    meta: { guestOnly: true }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'notFound',
    component: () => import('../views/NotFoundView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

// Navigation guards
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token')
  const userStr = localStorage.getItem('user')
  const isAuthenticated = !!token
  let userRole = ''

  if (userStr) {
    try {
      const user = JSON.parse(userStr)
      userRole = user.role || ''
    } catch (e) {
      // Invalid user data
    }
  }

  const isAdmin = userRole === 'admin'
  const isRenter = userRole === 'renter' || userRole === 'admin' // Admin can also access renter pages

  // Check if route requires auth
  if (to.meta.requiresAuth && !isAuthenticated) {
    next({ name: 'login', query: { redirect: to.fullPath } })
    return
  }

  // Check if route requires admin
  if (to.meta.requiresAdmin && !isAdmin) {
    next({ name: 'home' })
    return
  }

  // Check if route requires renter role
  if (to.meta.requiresRenter && !isRenter) {
    next({ name: 'apartments' })
    return
  }

  // Check if route is guest only
  if (to.meta.guestOnly && isAuthenticated) {
    next({ name: 'home' })
    return
  }

  next()
})

export default router