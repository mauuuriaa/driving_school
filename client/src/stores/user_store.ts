import {defineStore} from "pinia";
import axios from "axios"; 
import { onBeforeMount, ref, computed } from "vue";
import Cookies from 'js-cookie'; 
 
export const useUserStore = defineStore("userStore", () => { 
    const userInfo = ref({}); 
    const username = ref(); 
    const is_authenticated = ref(null); 
    const is_second_factor_active = ref(false);
    const is_superuser = ref(false); 
    const is_staff = ref(false);

    
    const can_edit_or_delete_students = computed(() => {
        return is_superuser.value || (is_authenticated.value && is_second_factor_active.value);
    });

    const can_export_data = computed(() => {
        
        return is_staff.value || is_superuser.value || (is_authenticated.value && is_second_factor_active.value);
    });

    
    async function fetchUserInfo() { 
        
        const r = await axios.get("/api/users/my/"); 
        userInfo.value = r.data; 
        username.value = r.data.username; 
        is_authenticated.value = r.data.is_authenticated; 
                
            
        is_second_factor_active.value = r.data.second_factor_active || false; 
        is_superuser.value = r.data.is_superuser || false;
        is_staff.value = r.data.is_staff || false; 
                
        axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken"); 
        
    }
    
    onBeforeMount(async() => { fetchUserInfo() }); 
    
    return { 
        userInfo, 
        is_authenticated, 
        username, 
        is_second_factor_active, 
        is_superuser,
        can_edit_or_delete_students,
        is_staff,
        can_export_data,
        fetchUserInfo 
    }
});