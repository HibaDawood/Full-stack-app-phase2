// translations/en.ts
import { TranslationKeys } from '../types/i18n';

export const en: TranslationKeys = {
  // Common
  appTitle: 'Todo App',
  welcome: 'Welcome',
  loading: 'Loading...',
  error: 'Error',
  save: 'Save',
  cancel: 'Cancel',
  delete: 'Delete',
  edit: 'Edit',
  create: 'Create',
  search: 'Search',
  filter: 'Filter',
  reset: 'Reset',
  language: 'Language',

  // Authentication
  signIn: 'Sign In',
  signUp: 'Sign Up',
  signOut: 'Sign Out',
  email: 'Email',
  password: 'Password',
  confirmPassword: 'Confirm Password',
  alreadyHaveAccount: 'Already have an account?',
  dontHaveAccount: 'Don\'t have an account?',
  createAccount: 'Create an account to get started',
  welcomeBack: 'Welcome back!',
  signInToAccount: 'Please sign in to your account',
  passwordMinLength: 'Password must be at least 8 characters long',
  passwordsMatch: 'Passwords do not match',
  validEmail: 'Please enter a valid email address',

  // Tasks
  yourTasks: 'Your Tasks',
  allTasks: 'All Tasks',
  pendingTasks: 'Pending Tasks',
  inProgress: 'In Progress',
  completedTasks: 'Completed Tasks',
  noTasks: 'No tasks found. Create your first task!',
  noPending: 'No pending tasks',
  noInProgress: 'No tasks in progress',
  noCompleted: 'No completed tasks yet',
  createFirstTask: 'Create your first task!',
  taskTitle: 'Task Title',
  taskDescription: 'Description',
  taskStatus: 'Status',
  deleteConfirmation: 'Are you sure you want to delete this task?',

  // Status options
  statusAll: 'All Tasks',
  statusPending: 'Pending',
  statusInProgress: 'In Progress',
  statusCompleted: 'Completed',

  // Filters
  filterByStatus: 'Filter by Status',
  searchPlaceholder: 'Search by title or description...',
};