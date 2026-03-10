import { Toast } from "@/components/widgets";
import { createContext, useRef, useContext, useState } from "react"
import { StyleSheet, View, Animated, Easing } from "react-native";

export const ToastContext = createContext<ToastContextType | undefined>(undefined);

type ToastParams = {
  title?: string;
  subtitle?: string;
  type?: 'info' | 'error' | 'success';
  duration?: number;
}

type ToastContextType = {
  showToast: (params: ToastParams) => void;
}

export function ToastProvider ({ children }: any) {

  const position = useRef(new Animated.Value(-200)).current;

  const [toast, setToast] = useState<ToastParams>({
    // Empty as long as no params are mandatory.
  });

  function showToast ({
    title,
    subtitle,
    type='info',
    duration=3000
  }: ToastParams) {

    setToast({
      title,
      subtitle,
      type
    })

    Animated.sequence([
      Animated.timing(position, {
        toValue: 0,
        duration: 200,
        easing: Easing.out(Easing.ease),
        useNativeDriver: true,
      }),

      Animated.delay(duration),

      Animated.timing(position, {
        toValue: -200,
        duration: 200,
        easing: Easing.ease,
        useNativeDriver: true,
      }),
    ]).start();
  }

  return (
    <ToastContext.Provider
      value={{
        showToast,
      }}
    >
      {children}
      <View style={StyleSheet.absoluteFill}>
        <Animated.View
          style={{
            transform: [{ translateY: position }],
          }}
        >
          <Toast
            title={toast.title}
            subtitle={toast.subtitle}
            type={toast.type}
          />
        </Animated.View>
      </View>
    </ToastContext.Provider>
  )
}

export function useToast () {
  const context = useContext(ToastContext);
  if (!context) {
    throw new Error('useToast must be used within an ToastProvider')
  }
  return context;
}