int main()
{
    E();
 
    if (l == '$')
        printf("Parsed successfully");
}
 
E'()  
{
    if (l == '+') {
        match('+');
        match('i');
        E'();
    }//The second condition of E'
    else if ( l == 'e' )
    {
      match('e');
    }
        return ();
}

match(char t)
{
    if (l == t) {
        l = getchar();
    }
    else
        printf("Error");
}
