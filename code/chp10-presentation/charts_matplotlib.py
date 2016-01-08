import matplotlib.pyplot as plt

# NOTE: You'll need to have the 'africa_cpi_cl' table and 'highest_cpi_cl'
# table we worked on in Chapter 9.

plt.plot(africa_cpi_cl.columns['CPI 2013 Score'],
         africa_cpi_cl.columns['Total (%)'])
plt.xlabel('CPI Score - 2013')
plt.ylabel('Child Labor Percentage')
plt.title('CPI & Child Labor Correlation')
plt.show()


plt.plot(highest_cpi_cl.columns['CPI 2013 Score'],
         highest_cpi_cl.columns['Total (%)'])
plt.xlabel('CPI Score - 2013')
plt.ylabel('Child Labor Percentage')
plt.title('CPI & Child Labor Correlation')
plt.show()
