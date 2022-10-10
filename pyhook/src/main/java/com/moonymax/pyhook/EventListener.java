package com.moonymax.pyhook;

public interface EventListener {
    Object onEvent(Object pluginRef, Object eventName, Object mainObject);
}