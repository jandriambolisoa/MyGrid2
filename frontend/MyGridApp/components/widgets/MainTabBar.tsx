import { View, TouchableOpacity, Text, StyleSheet, PanResponder } from 'react-native';
import { BottomTabBarProps } from "@react-navigation/bottom-tabs";
import { useEffect, useRef } from "react";

export function MainTabBar ({
  state,
  descriptors,
  navigation,
  insets
}: BottomTabBarProps) {

  const indexRef = useRef(state.index);
  const lastIndex = state.routes.length - 1;

  useEffect(() => {
    indexRef.current = state.index;
  }, [state.index])
  
  const panResponder = useRef(
    PanResponder.create({
      onStartShouldSetPanResponder: () => true,
      onPanResponderRelease: (e, gesture) => {

        if (gesture.dx > 50 && indexRef.current > 0) {
          // Swipe right → go to previous tab
          navigation.navigate(state.routes[indexRef.current - 1].name);
        } else if (gesture.dx < -50 && indexRef.current < lastIndex) {
          // Swipe left → go to next tab
          navigation.navigate(state.routes[indexRef.current + 1].name);
        }
      },
    })
  ).current;

  return (
    <View style={ [StyleSheet.absoluteFill, { justifyContent: 'flex-end' }] } {...panResponder.panHandlers}>
      <View style={{ flexDirection: 'row', paddingBottom: insets.bottom, paddingTop: 10, backgroundColor: '#fff' }}>
        {state.routes.map((route, index) => {
          const isFocused = state.index === index;

          const onPress= () => {
            navigation.navigate(route.name);
          }

          const { options } = descriptors[route.key];
          const label = options.title ?? route.name;

          return (
            <TouchableOpacity key={route.key} onPress={onPress} style={{ flex: 1, alignItems: 'center'}}>
              <Text style={{ color: isFocused ? 'tomato' : 'gray'}}>
                {label}
              </Text>
            </TouchableOpacity>
          )
        })}
      </View>
    </View>
  )
}