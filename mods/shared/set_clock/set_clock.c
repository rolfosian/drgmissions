#include <windows.h>
#include <lua.h>
#include <lauxlib.h>
#include <lualib.h>

// gcc -shared -o set_clock.dll set_clock.c -Iinclude -Wl,-Bstatic -llua

static int SetSystemClock(int year, int month, int day, int hour, int minute, int second) {
    SYSTEMTIME st;

    st.wYear = year;
    st.wMonth = month;
    st.wDay = day;
    st.wHour = hour;
    st.wMinute = minute;
    st.wSecond = second;
    st.wMilliseconds = 0;

    return SetSystemTime(&st);
}

static int l_SetSystemClock(lua_State *L) {
    int year = (int)lua_tonumber(L, 1);
    int month = (int)lua_tonumber(L, 2);
    int day = (int)lua_tonumber(L, 3);
    int hour = (int)lua_tonumber(L, 4);
    int minute = (int)lua_tonumber(L, 5);
    int second = (int)lua_tonumber(L, 6);

    lua_pushboolean(L, SetSystemClock(year, month, day, hour, minute, second));
    return 1;
}

static const struct luaL_Reg set_clock [] = {
    {"SetSystemClock", l_SetSystemClock},
    {NULL, NULL}
};

__declspec(dllexport) int luaopen_set_clock(lua_State *L) {
    luaL_newmetatable(L, "set_clock");
    luaL_setfuncs(L, set_clock, 0);
    return 1;
}