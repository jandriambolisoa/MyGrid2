import { useEffect, useRef } from "react";
import { Animated } from "react-native";

export function Reaction ({
  item,
  startY=35,
  endY=-35,
  right='50%',
  duration=2000,
} : {
  item: any;
  startY?: number;
  endY?: number;
  right?: string;
  duration?: number;
}) {

  const translateX = useRef(new Animated.Value(0)).current;
  const translateY = useRef(new Animated.Value(0)).current;
  const randScale = useRef(new Animated.Value(0)).current;
  const randRot = useRef(new Animated.Value(0)).current;

  const mountedRef = useRef(false);

useEffect(() => {
  let cancelled = false;

  const animate = () => {
    if (cancelled) return;

    // reset Y
    translateY.setValue(startY);

    // nouvelles valeurs aléatoires
    translateX.setValue(Math.random() * 100 - 50);
    randScale.setValue(Math.random() / 2 + 1);
    randRot.setValue(Math.random() * 20 - 10);

    // animation Y
    Animated.timing(translateY, {
      toValue: endY,
      duration: duration + Math.random() * duration / 2,
      delay: mountedRef.current ? 0 : Math.random() * duration,
      useNativeDriver: true,
    }).start(() => {
      mountedRef.current = true;
      animate(); // relance la boucle
    });
  };

  animate();

  return () => {
    cancelled = true; // stoppe la boucle si le composant se démonte
  };
}, []);

  return (
    <Animated.Text
      style={{
        position: "absolute",
        right: right as any,
        transform: [
          { translateX: translateX },
          { translateY: translateY },
          { scale: randScale },
          { rotate: randRot.interpolate({
              inputRange: [-10, 10],
              outputRange: ['-10deg', '10deg']
            })
          }
        ]
      }}
    >
      {item.reaction}
    </Animated.Text>
  );
}