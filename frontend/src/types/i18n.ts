// types/i18n.ts
export type Language = 'en' | 'zh';

export interface TranslationKeys {
  // Common
  appTitle: string;
  welcome: string;
  loading: string;
  error: string;
  save: string;
  cancel: string;
  delete: string;
  edit: string;
  create: string;
  search: string;
  filter: string;
  reset: string;
  language: string;

  // Authentication
  signIn: string;
  signUp: string;
  signOut: string;
  email: string;
  password: string;
  confirmPassword: string;
  alreadyHaveAccount: string;
  dontHaveAccount: string;
  createAccount: string;
  welcomeBack: string;
  signInToAccount: string;
  passwordMinLength: string;
  passwordsMatch: string;
  validEmail: string;

  // Tasks
  yourTasks: string;
  allTasks: string;
  pendingTasks: string;
  inProgress: string;
  completedTasks: string;
  noTasks: string;
  noPending: string;
  noInProgress: string;
  noCompleted: string;
  createFirstTask: string;
  taskTitle: string;
  taskDescription: string;
  taskStatus: string;
  deleteConfirmation: string;

  // Status options
  statusAll: string;
  statusPending: string;
  statusInProgress: string;
  statusCompleted: string;

  // Filters
  filterByStatus: string;
  searchPlaceholder: string;
}