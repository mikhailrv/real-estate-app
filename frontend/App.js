import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View } from 'react-native';
import React from 'react';
import { NavigationContainer } from '@react-navigation/native'; 
import { createStackNavigator } from '@react-navigation/stack'; 
import AuthScreen from './screens/auth_screen'; 
import HomeScreen from './screens/home_screen'; 
import ProfileScreen from './screens/profile_screen'; 
import FavoritesScreen from './screens/favorites_screen'; 
import 'react-native-gesture-handler';
import ChatsScreen from './screens/chats_screen'; 
import ListingDetailsScreen from './screens/listing_details_screen';
const Stack = createStackNavigator(); 

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen name="Login" component={AuthScreen} />
        <Stack.Screen name="Register" component={AuthScreen} />
        <Stack.Screen name="Home" component={HomeScreen} />
        <Stack.Screen name="Profile" component={ProfileScreen} />
        <Stack.Screen name="Favorites" component={FavoritesScreen} />
        <Stack.Screen name="Chats" component={ChatsScreen} />
        <Stack.Screen name="ListingDetails" component={ListingDetailsScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}


const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});



